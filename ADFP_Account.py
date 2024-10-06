import os
import shutil
import portalocker
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory, abort, make_response, send_file
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = './uploads/'  # 暂存文件的目录
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_file(file, folder, filename):
    file_path = os.path.join(folder, filename)
    file.save(file_path)
    return file_path

def move_file(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.move(src, dest)

def read_key_file_with_lock(key_path):
    """读取带有共享锁定的密钥文件"""
    with open(key_path, 'rb') as key_file:
        portalocker.lock(key_file, portalocker.LOCK_SH)  # 获取共享锁
        key_data = key_file.read()
        portalocker.unlock(key_file)
    return key_data

def read_credentials(adfp_path, vpn_path, account_name):
    """读取 ADFP 和 VPN 凭据，假设 ADFP 帐号与 VPN 帐号相同"""
    # 检查文件是否存在
    if not os.path.exists(adfp_path):
        return None, None, None, None, f"未找到 ADFP 檔案: {adfp_path}"
    if not os.path.exists(vpn_path):
        return None, None, None, None, f"未找到 VPN 檔案: {vpn_path}"

    try:
        # 读取 ADFP 文件
        adfp_df = pd.read_excel(adfp_path)
        adfp_info = adfp_df[adfp_df['Account'] == account_name]
        if adfp_info.empty:
            return None, None, None, None, f"在 ADFP 檔案中未找到帳號: {account_name}"
        adfp_password = adfp_info['Password'].values[0]

        # 读取 VPN 文件
        vpn_df = pd.read_excel(vpn_path)
        vpn_info = vpn_df[vpn_df['Account'] == account_name]
        if vpn_info.empty:
            return None, None, None, None, f"在 VPN 檔案中未找到帳號: {account_name}"
        vpn_password = vpn_info['Password'].values[0]

        return account_name, adfp_password, account_name, vpn_password, None

    except Exception as e:
        return None, None, None, None, f"讀取憑據時發生錯誤: {str(e)}"
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    account_type = request.form.get('account_type')
    account_name = request.form.get('account_name')
    student_id = request.form.get('student_id')
    name = request.form.get('name')
    email = request.form.get('email')
    course_code = request.form.get('course_code')
    semester = request.form.get('semester')
    lab_code = request.form.get('lab_code')
    key_file = request.files['key_file']

    # 定义锁文件目录
    if account_type == 'course':
        lock_final_folder = f"./COURSE/{semester}/{course_code}/LOCK/"
    else:
        lock_final_folder = f"./LAB/{lab_code}/LOCK/"

    # 检查是否已经有锁文件
    lock_file_path = os.path.join(lock_final_folder, f"{account_name}.lock")
    if os.path.exists(lock_file_path):
        flash("該帳號已被綁定，如果非本人綁定，請聯繫管理員解鎖。", "error")
        return redirect(url_for('home'))

    # 检查密钥文件是否存在并使用共享锁读取
    if account_type == 'course':
        key_path = f"./COURSE/{semester}/{course_code}/{semester}_{course_code}.key"
    else:
        key_path = f"./LAB/{lab_code}/{lab_code}.key"

    if not os.path.exists(key_path):
        flash("未找到相關課程資訊，請確認資訊填寫正確。", "error")
        return redirect(url_for('home'))

    try:
        expected_key_data = read_key_file_with_lock(key_path)
    except Exception as e:
        flash(f"读取密钥文件时出错: {str(e)}", "error")
        return redirect(url_for('home'))

    # 验证上传的密钥文件
    if not key_file or key_file.read() != expected_key_data:
        flash("金鑰認證錯誤", "error")
        return redirect(url_for('home'))

    # 保存用户信息到会话中以供下一步使用
    session['account_type'] = account_type
    session['account_name'] = account_name
    session['student_id'] = student_id
    session['name'] = name
    session['email'] = email
    session['semester'] = semester
    session['course_code'] = course_code
    session['lab_code'] = lab_code

    # 设置认证标志
    session['authenticated'] = True

    # 一切都通过，跳转到上传文件页面
    return redirect(url_for('upload_documents'))

@app.route('/upload_documents', methods=['GET', 'POST'])
def upload_documents():
    # 检查认证标志
    if not session.get('authenticated'):
        flash("請先完成金鑰認證。", "error")
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # 获取会话中的信息
        account_type = session.get('account_type')
        account_name = session.get('account_name')
        name = session.get('name')

        # 文件名
        stu_filename = f"{account_name}_{name}_stu.png"
        nda_filename = f"{account_name}_{name}_NDA.png"

        # 暂存文件路径
        stu_temp_path = os.path.join(UPLOAD_FOLDER, stu_filename)
        nda_temp_path = os.path.join(UPLOAD_FOLDER, nda_filename)

        # 检查暂存文件是否存在
        if not os.path.exists(stu_temp_path) or not os.path.exists(nda_temp_path):
            flash("請記得點選「上傳」在學證明和NDA文件。", "error")
            return redirect(url_for('upload_documents'))

        # 确定最终保存路径
        if account_type == 'course':
            stu_final_folder = f"./COURSE/{session['semester']}/{session['course_code']}/STU/"
            nda_final_folder = f"./COURSE/{session['semester']}/{session['course_code']}/NDA/"
        else:
            stu_final_folder = f"./LAB/{session['lab_code']}/STU/"
            nda_final_folder = f"./LAB/{session['lab_code']}/NDA/"

        # 移动文件到最终目录
        move_file(stu_temp_path, os.path.join(stu_final_folder, stu_filename))
        move_file(nda_temp_path, os.path.join(nda_final_folder, nda_filename))

        # 成功上传，跳转到确认绑定页面
        return redirect(url_for('success'))

    return render_template('upload_documents.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    file_type = request.form.get('file_type')
    file = request.files.get('file')
    account_name = session.get('account_name')
    name = session.get('name')

    # 检查文件名是否正确
    if file_type == 'stu_file':
        expected_filename = f"{account_name}_{name}_stu.png"
    elif file_type == 'nda_file':
        expected_filename = f"{account_name}_{name}_NDA.png"
    else:
        return jsonify({'error': 'Invalid file type'}), 400

    if file.filename != expected_filename:
        return jsonify({'error': f'文件名稱錯誤，應該為 {expected_filename}'}), 400

    # 保存文件到临时上传目录
    temp_path = save_file(file, UPLOAD_FOLDER, expected_filename)

    # 返回相对路径用于前端预览
    return jsonify({'file_path': url_for('uploaded_file', filename=expected_filename)})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/success')
def success():
    # 检查认证标志
    if not session.get('authenticated'):
        flash("請先完成金鑰認證。", "error")
        return redirect(url_for('home'))
    
    account_type = session.get('account_type')
    account_name = session.get('account_name')
    student_id = session.get('student_id')
    name = session.get('name')
    email = session.get('email')
    semester = session.get('semester')
    course_code = session.get('course_code')
    lab_code = session.get('lab_code')

    if account_type == 'course':
        base_path = './COURSE'
        adfp_path = os.path.join(base_path, semester, course_code, f"{semester}_{course_code}_ADFP.xlsx")
        vpn_path = os.path.join(base_path, semester, course_code, f"{semester}_{course_code}_VPN.xlsx")
        lock_final_folder = f"./COURSE/{semester}/{course_code}/LOCK/"
        info_folder = f"./COURSE/{semester}/{course_code}/INFO/"
    elif account_type == 'lab':
        base_path = './LAB'
        adfp_path = os.path.join(base_path, lab_code, f"{lab_code}_ADFP.xlsx")
        vpn_path = os.path.join(base_path, lab_code, f"{lab_code}_VPN.xlsx")
        lock_final_folder = f"./LAB/{lab_code}/LOCK/"
        info_folder = f"./LAB/{lab_code}/INFO/"
    else:
        flash("未知的帳號類型。", "error")
        return redirect(url_for('home'))

    # 读取凭据
    adfp_account, adfp_password, vpn_account, vpn_password, error = read_credentials(adfp_path, vpn_path, account_name)

    if error:
        flash(error, "error")
        return redirect(url_for('home'))

    # 生成锁文件
    os.makedirs(lock_final_folder, exist_ok=True)
    lock_file_path = os.path.join(lock_final_folder, f"{account_name}.lock")
    with open(lock_file_path, 'w') as lock_file:
        lock_file.write("Account locked")

    session['adfp_account'] = adfp_account
    session['adfp_password'] = adfp_password
    session['vpn_account'] = vpn_account
    session['vpn_password'] = vpn_password

    # 保存用户信息到 Excel 文件
    os.makedirs(info_folder, exist_ok=True)
    info_file_path = os.path.join(info_folder, f"{account_name}_info.xlsx")

    user_data = {
        'Account Type': [account_type],
        'Account Name': [account_name],
        'Student ID': [student_id],
        'Name': [name],
        'Email': [email],
        'Semester': [semester],
        'Course Code': [course_code],
        'Lab Code': [lab_code],
        'ADFP Account': [adfp_account],
        'ADFP Password': [adfp_password],
        'VPN Account': [vpn_account],
        'VPN Password': [vpn_password]
    }

    df = pd.DataFrame(user_data)
    df.to_excel(info_file_path, index=False)

    return render_template('success.html', name=name, adfp_account=adfp_account, adfp_password=adfp_password,
                           vpn_account=vpn_account, vpn_password=vpn_password)

@app.route('/download_credentials')
def download_credentials():
    adfp_account = session.get('adfp_account')
    adfp_password = session.get('adfp_password')
    vpn_account = session.get('vpn_account')
    vpn_password = session.get('vpn_password')
    name = session.get('name')
    account_name = session.get('account_name')

    if not all([adfp_account, adfp_password, vpn_account, vpn_password]):
        flash("無法找到完整的憑據信息。", "error")
        return redirect(url_for('home'))

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    data = {
        'Account Type': ['ADFP', 'VPN'],
        'Account': [adfp_account, vpn_account],
        'Password': [adfp_password, vpn_password]
    }
    df = pd.DataFrame(data)
    df.to_excel(writer, index=False, sheet_name='Credentials')

    writer.close()
    output.seek(0)

    filename = f"{account_name}_credentials.xlsx"

    return send_file(output, download_name=filename, as_attachment=True)

@app.route('/logout')
def logout():
    session.clear()
    flash("您已成功登出。", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
