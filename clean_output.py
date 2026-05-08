
import os, shutil, sys, traceback

output_dir = "/mnt/g/autoblogs-master/autoblogs-master/output"

def safe_delete_dir(path):
    """递归安全删除目录内容：文件使用 os.unlink，子目录使用 shutil.rmtree，捕获一切错误并记录。"""
    try:
        for entry in os.scandir(path):
            if entry.is_file() or entry.is_symlink():
                try:
                    os.unlink(entry.path)
                except Exception as e:
                    print(f"Failed to delete file {entry.path}: {e}", file=sys.stderr)
            elif entry.is_dir():
                try:
                    shutil.rmtree(entry.path)
                except Exception as e:
                    print(f"Failed to delete directory {entry.path}: {e}", file=sys.stderr)
        print(f"Successfully cleared {path}")
    except Exception as e:
        print(f"Error during safe delete: {e}", file=sys.stderr)
        traceback.print_exc()

if __name__ == "__main__":
    safe_delete_dir(output_dir)
