import customtkinter as ctk
import tkinter.messagebox as messagebox
import arabic_reshaper
from bidi.algorithm import get_display
import sys
import os
import psutil
import ctypes
import subprocess
import platform
import threading
import tempfile
import time
import pycdlib

def render_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

class BootableUSBCreatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("أداة إنشاء أقراص الإقلاع")
        self.geometry("500x500")
        self.resizable(False, False)

        # Configure appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.setup_ui()

    def setup_ui(self):
        # Title Label
        self.title_label = ctk.CTkLabel(self, text=render_arabic("أداة إنشاء أقراص الإقلاع (Bootable USB Creator)"), font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=20)

        # USB Drive Selection
        self.usb_frame = ctk.CTkFrame(self)
        self.usb_frame.pack(pady=10, padx=20, fill="x")

        self.usb_label = ctk.CTkLabel(self.usb_frame, text=render_arabic("اختيار قرص USB:"))
        self.usb_label.pack(side="right", padx=10)

        self.usb_dropdown = ctk.CTkComboBox(self.usb_frame, values=[render_arabic("جاري البحث...")], state="readonly")
        self.usb_dropdown.pack(side="left", expand=True, fill="x", padx=10)

        self.refresh_btn = ctk.CTkButton(self.usb_frame, text=render_arabic("تحديث"), width=60, command=self.refresh_drives)
        self.refresh_btn.pack(side="left", padx=5)

        # ISO Selection
        self.iso_frame = ctk.CTkFrame(self)
        self.iso_frame.pack(pady=10, padx=20, fill="x")

        self.iso_label = ctk.CTkLabel(self.iso_frame, text=render_arabic("ملف الـ ISO:"))
        self.iso_label.pack(side="right", padx=10)

        self.iso_path_var = ctk.StringVar()
        self.iso_entry = ctk.CTkEntry(self.iso_frame, textvariable=self.iso_path_var, state="readonly")
        self.iso_entry.pack(side="left", expand=True, fill="x", padx=10)

        self.browse_btn = ctk.CTkButton(self.iso_frame, text=render_arabic("تصفح"), width=60, command=self.browse_iso)
        self.browse_btn.pack(side="left", padx=5)

        # Partition Scheme
        self.scheme_frame = ctk.CTkFrame(self)
        self.scheme_frame.pack(pady=10, padx=20, fill="x")

        self.scheme_label = ctk.CTkLabel(self.scheme_frame, text=render_arabic("مخطط التقسيم (Partition Scheme):"))
        self.scheme_label.pack(side="right", padx=10)

        self.scheme_var = ctk.StringVar(value="MBR")
        self.mbr_radio = ctk.CTkRadioButton(self.scheme_frame, text="MBR (Legacy)", variable=self.scheme_var, value="MBR")
        self.mbr_radio.pack(side="right", padx=10)

        self.gpt_radio = ctk.CTkRadioButton(self.scheme_frame, text="GPT (UEFI)", variable=self.scheme_var, value="GPT")
        self.gpt_radio.pack(side="right", padx=10)

        # Status and Progress
        self.status_label = ctk.CTkLabel(self, text=render_arabic("جاهز"), text_color="green")
        self.status_label.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.set(0)

        # Start Button
        self.start_btn = ctk.CTkButton(self, text=render_arabic("ابدأ الحرق (Start)"), font=ctk.CTkFont(size=16, weight="bold"), command=self.start_process)
        self.start_btn.pack(pady=20, padx=20, fill="x")

    def check_admin_privileges(self):
        if platform.system() == "Windows":
            try:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            except:
                is_admin = False

            if not is_admin:
                messagebox.showerror(
                    render_arabic("صلاحيات مفقودة"),
                    render_arabic("الرجاء تشغيل البرنامج كمسؤول (Run as Administrator)")
                )
                self.start_btn.configure(state="disabled")
                return False
        elif platform.system() == "Linux":
            if os.geteuid() != 0:
                messagebox.showerror(
                    render_arabic("صلاحيات مفقودة"),
                    render_arabic("الرجاء تشغيل البرنامج بصلاحيات الرووت (sudo)")
                )
                self.start_btn.configure(state="disabled")
                return False
        return True

    def refresh_drives(self):
        self.usb_dropdown.configure(values=[render_arabic("جاري البحث...")])
        self.update()

        # Run drive detection in a separate thread so GUI doesn't freeze
        threading.Thread(target=self._detect_drives_thread, daemon=True).start()

    def _detect_drives_thread(self):
        usb_drives = []
        if platform.system() == "Windows":
            # Using wmic to get logical disks of MediaType 11 (Removable Media) or 12 (Fixed, but we must be careful)
            # A safer way in python is using psutil and checking options, but wmic is more reliable for "removable"
            try:
                output = subprocess.check_output(
                    ['wmic', 'logicaldisk', 'where', 'drivetype=2', 'get', 'deviceid,volumename,size'],
                    text=True
                )
                lines = output.strip().split('\n')[1:]
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        drive_letter = parts[0]
                        usb_drives.append(f"{drive_letter} (USB)")
            except Exception as e:
                print(f"Error getting drives: {e}")
        elif platform.system() == "Linux":
            try:
                output = subprocess.check_output(
                    ['lsblk', '-o', 'NAME,TRAN,SIZE', '-nl'],
                    text=True
                )
                for line in output.split('\n'):
                    if 'usb' in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            usb_drives.append(f"/dev/{parts[0]} - {parts[2]}")
            except Exception as e:
                print(f"Error getting drives: {e}")

        if not usb_drives:
            usb_drives = [render_arabic("لا يوجد قرص USB")]

        # Update GUI from main thread
        self.after(0, self._update_drives_dropdown, usb_drives)

    def _update_drives_dropdown(self, drives):
        self.usb_dropdown.configure(values=drives)
        if drives:
            self.usb_dropdown.set(drives[0])

    def browse_iso(self):
        filename = ctk.filedialog.askopenfilename(
            title=render_arabic("اختر ملف ISO"),
            filetypes=[("ISO Files", "*.iso"), ("All Files", "*.*")]
        )
        if filename:
            self.iso_path_var.set(filename)

    def start_process(self):
        usb_drive = self.usb_dropdown.get()
        iso_file = self.iso_path_var.get()
        scheme = self.scheme_var.get()

        if render_arabic("لا يوجد") in usb_drive or render_arabic("جاري") in usb_drive:
            messagebox.showwarning(render_arabic("تنبيه"), render_arabic("الرجاء اختيار قرص USB صحيح"))
            return

        if not iso_file or not os.path.exists(iso_file):
            messagebox.showwarning(render_arabic("تنبيه"), render_arabic("الرجاء اختيار ملف ISO صحيح"))
            return

        # Warning
        msg = render_arabic(f"تحذير: سيتم مسح جميع البيانات الموجودة على القرص '{usb_drive}' نهائياً.\nهل تريد الاستمرار؟")
        if not messagebox.askyesno(render_arabic("تأكيد التهيئة"), msg, icon='warning'):
            return

        self.start_btn.configure(state="disabled")
        self.status_label.configure(text=render_arabic("جاري التحضير..."), text_color="orange")
        self.progress_bar.set(0)

        # Extract drive letter or path
        drive_path = usb_drive.split()[0]

        threading.Thread(target=self._burn_process_thread, args=(drive_path, iso_file, scheme), daemon=True).start()

    def _get_windows_disk_number(self, drive_letter):
        try:
            output = subprocess.check_output(
                ['wmic', 'logicaldisk', 'where', f'deviceid="{drive_letter}:"', 'assoc', '/assocclass:Win32_LogicalDiskToPartition'],
                text=True
            )
            # Output will contain something like Disk #1, Partition #0
            for line in output.split('\n'):
                if "Disk #" in line:
                    parts = line.split('Disk #')
                    if len(parts) > 1:
                        return parts[1].split(',')[0].strip()
        except Exception:
            pass
        return None

    def _burn_process_thread(self, drive_path, iso_file, scheme):
        try:
            self._update_status("جاري تهيئة القرص...", 0.1)

            # Check ISO size to decide filesystem
            iso_size = os.path.getsize(iso_file)
            fs_type = "NTFS" if iso_size > 4000000000 else "FAT32"

            if platform.system() == "Windows":
                drive_letter = drive_path.replace(":", "")

                disk_num = self._get_windows_disk_number(drive_letter)
                if disk_num is None:
                    # Fallback to volume format if we can't find the physical disk
                    diskpart_script = (
                        f"select volume {drive_letter}\n"
                        f"format fs={fs_type} quick\n"
                        "exit\n"
                    )
                else:
                    partition_cmd = "convert gpt\n" if scheme == "GPT" else "convert mbr\n"
                    active_cmd = "active\n" if scheme == "MBR" else ""

                    diskpart_script = (
                        f"select disk {disk_num}\n"
                        "clean\n"
                        f"{partition_cmd}"
                        "create partition primary\n"
                        f"{active_cmd}"
                        f"format fs={fs_type} quick\n"
                        f"assign letter={drive_letter}\n"
                        "exit\n"
                    )

                # Write to temp file and run
                fd, script_path = tempfile.mkstemp(suffix=".txt")
                with os.fdopen(fd, 'w') as f:
                    f.write(diskpart_script)

                subprocess.run(["diskpart", "/s", script_path], capture_output=True, check=False)
                os.remove(script_path)

                target_extract_dir = f"{drive_letter}:\\"

            elif platform.system() == "Linux":
                # Ensure it's a device
                if drive_path.startswith("/dev/"):
                    # Unmount all partitions of the drive
                    subprocess.run(["umount", f"{drive_path}*"], shell=True, capture_output=True)

                    # Create partition table using parted
                    label_type = "gpt" if scheme == "GPT" else "msdos"
                    subprocess.run(["parted", "-s", drive_path, "mklabel", label_type], capture_output=True, check=False)

                    # Create a primary partition taking all space
                    subprocess.run(["parted", "-s", drive_path, "mkpart", "primary", "0%", "100%"], capture_output=True, check=False)

                    if scheme == "MBR":
                        subprocess.run(["parted", "-s", drive_path, "set", "1", "boot", "on"], capture_output=True, check=False)

                    # The partition device is usually drive_path + "1" (e.g. /dev/sdb1)
                    part_path = f"{drive_path}1"

                    # Format the new partition
                    if fs_type == "FAT32":
                        subprocess.run(["mkfs.vfat", "-F", "32", part_path], capture_output=True, check=False)
                    else:
                        subprocess.run(["mkfs.ntfs", "-Q", part_path], capture_output=True, check=False)

                    # Mount it to copy files
                    mnt_dir = tempfile.mkdtemp()
                    subprocess.run(["mount", part_path, mnt_dir], capture_output=True, check=False)
                    target_extract_dir = mnt_dir
                else:
                    raise Exception("مسار القرص غير صحيح")

            self._update_status("جاري استخراج ملفات ISO...", 0.3)

            # Using pycdlib for robust ISO extraction
            import pycdlib
            iso = pycdlib.PyCdlib()
            iso.open(iso_file)

            # Check what extensions we have
            has_udf = iso.has_udf()
            has_joliet = iso.has_joliet()
            has_rr = iso.has_rock_ridge()

            facade = None
            if has_udf:
                facade = iso.get_udf_facade()
            elif has_joliet:
                facade = iso.get_joliet_facade()
            elif has_rr:
                facade = iso.get_rock_ridge_facade()
            else:
                facade = iso.get_iso9660_facade()

            for dirname, _, filelist in facade.walk('/'):
                # Create corresponding directory
                # dirname in pycdlib often comes with a leading slash
                rel_dir = dirname.lstrip('/')
                target_dir = os.path.join(target_extract_dir, rel_dir)
                os.makedirs(target_dir, exist_ok=True)

                for filename in filelist:
                    # Sometimes pycdlib appends ;1, we strip it for disk
                    target_filename = filename.split(';')[0] if ';' in filename else filename

                    target_file_path = os.path.join(target_dir, target_filename)
                    iso_file_path = f"{dirname}/{filename}" if dirname != '/' else f"/{filename}"

                    with open(target_file_path, "wb") as f:
                        facade.get_file_from_iso_fp(f, iso_file_path)

            iso.close()

            self._update_status(f"جاري نسخ الملفات (100%)...", 0.8)

            self._update_status("جاري إنشاء قطاع الإقلاع (Boot Sector)...", 0.9)

            if platform.system() == "Windows":
                # Use bootsect to make it bootable (requires admin)
                # bootsect.exe /nt60 X: /mbr
                subprocess.run(["bootsect.exe", "/nt60", f"{drive_letter}:", "/mbr", "/force"], capture_output=True)
            elif platform.system() == "Linux":
                # Unmount after copying
                subprocess.run(["umount", target_extract_dir], capture_output=True)
                os.rmdir(target_extract_dir)

                # In Linux, syslinux is commonly used for FAT32
                # Note: this requires syslinux to be installed on the system and works on the partition
                if scheme == "MBR" and fs_type == "FAT32":
                    subprocess.run(["syslinux", "-i", part_path], capture_output=True, check=False)

            self._update_status("اكتملت العملية بنجاح!", 1.0, "green")

        except Exception as e:
            self._update_status(f"حدث خطأ: {str(e)}", 0.0, "red")

        finally:
            self.after(0, lambda: self.start_btn.configure(state="normal"))

    def _update_status(self, text, progress, color="orange"):
        self.after(0, lambda: self.status_label.configure(text=render_arabic(text), text_color=color))
        self.after(0, lambda: self.progress_bar.set(progress))

if __name__ == "__main__":
    app = BootableUSBCreatorApp()
    app.check_admin_privileges()
    app.refresh_drives()

    # Just running in background to test import, do not start mainloop if test mode
    if len(sys.argv) > 1 and sys.argv[1] == "--test-mode":
        print("Test mode completed.")
    else:
        app.mainloop()
