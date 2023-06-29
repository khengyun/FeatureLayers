import re
import fileinput
import subprocess
from featurelayers.__version__ import __version__
import git
from rich import *
from pathlib import Path
from typing import List


def check_or_update_version(update:bool=False)-> str: # Kiểm tra và cập nhật version
    if not update:
        
        version = __version__
        print(f"Current version: {version}")
        return version
    
    else: # Cập nhật version
        # Tách version thành các phần tử số
        version_parts = list(map(int, version.split('.')))

        # Tăng giá trị cuối cùng lên 1
        version_parts[-1] += 1

        # Kiểm tra và điều chỉnh giá trị các phần tử
        for i in range(len(version_parts) - 1, 0, -1):
            if version_parts[i] > 9:
                version_parts[i] = 0
                version_parts[i - 1] += 1

        # Chuyển đổi lại thành chuỗi và gắn giá trị version mới
        new_version = '.'.join(map(str, version_parts))
        new_version_str = f'"{new_version}"'
        print(f"New version: {new_version}")
        # Đọc giá trị version từ module featurelayers
        # Lưu giá trị version vào file __version__
        print("Updating version local...")
        with fileinput.FileInput('./featurelayers/__version__.py', inplace=True) as file:
            for line in file:
                line = re.sub(r'__version__ = .*', f'__version__ = {new_version_str}', line.rstrip())
                print(line)

        # Cập nhật nội dung trong README với phiên bản mới nhất
        repo = git.Repo()
        readme_file = 'README.md'
        readme = Path(repo.working_dir) / readme_file

        # Đọc nội dung README
        with open(readme, 'r') as f:
            content = f.read()

        # Kiểm tra sự tồn tại của __version__
        if '__version__' not in content:
            # Thêm __version__ vào nội dung README
            new_content = content + f'\n__version__ = "{new_version_str}"\n'
        else:
            # Tìm và thay thế phiên bản cũ trong README bằng phiên bản mới
            new_content = re.sub(r'__version__ = ".*"', f'__version__ = "{new_version_str}"', content)

        # Ghi nội dung mới vào README
        with open(readme, 'w') as f:
            f.write(new_content)
        # Thực hiện add, commit và push với commit_message_with_version

        print("[bold green]README updated with the latest version![/bold green]")
                # Gắn giá trị version vào nội dung commit
        commit_message_with_version = f" (Version {new_version_str})"
        return commit_message_with_version


def check_git_status() -> List[str]:
    try:
        # Sử dụng lệnh git status để xem trạng thái của các file
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        output = result.stdout.strip()

        # Phân tích kết quả để lấy danh sách các file đã thay đổi và không nằm trong gitnone
        changed_files = []
        lines = output.split('\n')
    
        for line in lines:
            file_status = line[:2]
            file_path = line[3:]
            if file_status != '??':
                # File đã bị thay đổi và không nằm trong gitnone
                changed_files.append(file_path)
                
                
        return changed_files
    except subprocess.CalledProcessError as e:
        print(f"[bold red]Error: {e}[/bold red]")
        return []
    
def git_add_commit_push(message:dict={},changefile:list=[],all:bool=None): # Thực hiện git add, git commit và git push
    try:
        # Add all files to staging area
        if all:
            subprocess.run(["git", "add", "."], check=True)
        else:
            for file in changefile:
                subprocess.run(["git", "add", file], check=True)

        
        # Get username from git config
        username = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
        username = username.stdout.strip()
        message["description"] = f"Committed by {username}"
        # Append username to commit message
        subprocess.run(["git", "commit", "-m", message["title"], "-m", message["description"]], check=True)

        # Push to remote repository
        subprocess.run(["git", "push"], check=True)

        print("[bold green]Push successful![/bold green]")
    except subprocess.CalledProcessError as e:
        print(f"[bold red]Error: {e}[/bold red]")





def check_before_push():
    version:str = check_or_update_version() # Kiểm tra version
    git_status:List[str] = check_git_status() # Kiểm tra trạng thái git
    print("Git status: ")
    print(git_status)
            # Nhập nội dung commit từ người dùng
    commit_message:str = input("Enter Commit Content: ")
    message:dict = {
        "title": f"{commit_message}{version}",
        "description": ""
    }
    git_add_commit_push(message=message,changefile=git_status,all=True)
    
    
    print(git_status)
    # git_add_commit_push()
    






if __name__ == '__main__':
    check_before_push()
