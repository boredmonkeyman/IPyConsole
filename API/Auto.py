# -*- coding: utf-8 -*-
# Python Script, API Version = V241

import clr

clr.AddReference("System")
clr.AddReference("System.IO")
clr.AddReference("System.Threading")
clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")

from System import Type, Activator
from System.Drawing import Point as sysPoint, Size as sysSize
from System.Threading import Thread, ThreadStart, ApartmentState, CancellationTokenSource
from System.Windows.Forms import Application, Form, Label, TextBox, Button, OpenFileDialog, DialogResult, MessageBox, FolderBrowserDialog, MessageBoxButtons, GroupBox, RadioButton, CheckBox
from System.IO import File, Directory, FileInfo, Path

import sys
import re
import os
import traceback
import tempfile

class MainForm(Form):
    def __init__(self):
        # ����self.XmpViewer
        try:
            # Virtual Huamn Vision Lab --- VisionLabViewer.Application
            # Virtual Photometric Lab --- XmpViewer.Application
            self.theApp = Type.GetTypeFromProgID("VisionLabViewer.Application")
            if self.theApp is None:
                raise Exception("���Թ���Ա������С�Virtual Huamn Vision Lab��!")
            self.XmpViewer = Activator.CreateInstance(self.theApp)
        except Exception as e:
            self.handleError("��ʼ������", e)
            
        # ��־λ-��ֹ����
        self.stop_sim = False

        # ���崰��
        self.Name = "�Զ��������ʲ�ִ�е���ͼƬ"
        self.Text = "�Զ��������ʲ�ִ�е���ͼƬ"
        self.Width = 1000
        self.Height = 300
        self.TopMost = True
        
        # ѡ�� surface library path
        self.labelSurfaceLibrary = Label()
        self.labelSurfaceLibrary.Text = "surface library path:"
        self.labelSurfaceLibrary.Location = sysPoint(30, 10)
        self.labelSurfaceLibrary.Size = sysSize(180, 20)
        self.textBoxSurfaceLibrary = TextBox()
        self.textBoxSurfaceLibrary.Location = sysPoint(230, 10)
        self.textBoxSurfaceLibrary.Size = sysSize(430, 30)
        self.btnChooseSurfacePath = Button()
        self.btnChooseSurfacePath.Text = "��"
        self.btnChooseSurfacePath.Location = sysPoint(670, 10)
        self.btnChooseSurfacePath.Size = sysSize(28, 20)
        self.btnChooseSurfacePath.Click += self.setSurfacePath
        
        # ѡ�� volume library path:
        self.labelVolumeLibrary = Label()
        self.labelVolumeLibrary.Text = "volume library path:"
        self.labelVolumeLibrary.Location = sysPoint(30, 50)
        self.labelVolumeLibrary.Size = sysSize(180, 20)
        self.textBoxVolumeLibrary = TextBox()
        self.textBoxVolumeLibrary.Location = sysPoint(230, 50)
        self.textBoxVolumeLibrary.Size = sysSize(430, 30)
        self.btnChooseVolumePath = Button()
        self.btnChooseVolumePath.Text = "��"
        self.btnChooseVolumePath.Location = sysPoint(670, 50)
        self.btnChooseVolumePath.Size = sysSize(28, 20)  
        self.btnChooseVolumePath.Click += self.setVolumePath
        
        # ѡ�� ��ǰʹ�õ�scdocx �ļ�
        self.labelScDocxPath = Label()
        self.labelScDocxPath.Text = "scdocx file:"
        self.labelScDocxPath.Location = sysPoint(30, 90)
        self.labelScDocxPath.Size = sysSize(180, 20)
        self.textBoxScDocxPath = TextBox()
        self.textBoxScDocxPath.Location = sysPoint(230, 90)
        self.textBoxScDocxPath.Size = sysSize(430, 30)
        self.btnChooseScDocxPath = Button()
        self.btnChooseScDocxPath.Text = "��"
        self.btnChooseScDocxPath.Location = sysPoint(670, 90)
        self.btnChooseScDocxPath.Size = sysSize(28, 20)  
        self.btnChooseScDocxPath.Click += self.setScDocxPath
        
        # Radio�� ��ѡCPU/GPU����
        self.groupBox = GroupBox()
        self.groupBox.Location = sysPoint(750, 10)
        self.groupBox.Size = sysSize(200, 80)
        self.groupBox.Text = "CPU/GPU"
        
        # Radio Button CPU
        self.radio_btn_cpu = RadioButton() 
        self.radio_btn_cpu.Text = "CPU"
        self.radio_btn_cpu.Location = sysPoint(10, 20)
        self.radio_btn_cpu.Checked = True  # Ĭ�ϣ�CPU����
        
        # Radio Button GPU
        self.radio_btn_gpu = RadioButton() 
        self.radio_btn_gpu.Text = "GPU"
        self.radio_btn_gpu.Location = sysPoint(10, 40)
        
        # ��ֹѡ��
        self.label_pause = Label()
        self.label_pause.Text = "���ִ����Զ���ֹ"
        self.label_pause.Location = sysPoint(790, 110)
        self.label_pause.Size = sysSize(180, 20)
        self.checkbox_pause = CheckBox()
        self.checkbox_pause.Location = sysPoint(760, 100)
        self.checkbox_pause.Size = sysSize(30, 30)
        self.checkbox_pause.Checked = False  # Ĭ�ϣ�����������ֹ����
        
        # ��ť ִ�з���
        self.btnCompute = Button()
        self.btnCompute.Text = "��ʼִ��"
        self.btnCompute.Location = sysPoint(350, 160)
        self.btnCompute.Size = sysSize(180, 30)
        self.btnCompute.Click += self.compute
        
        # ��ʾ���·��
        self.labelInfo = Label()
        self.labelInfo.Location = sysPoint(30, 270)
        self.labelInfo.Size = sysSize(340, 30)
        
        # ·�������ļ�
        self.outpath = ""
        self.configFile = os.path.join(tempfile.gettempdir(), "zhanshengconfig.txt")
        self.errorlogFile = os.path.join(tempfile.gettempdir(), "zhanshengerrorlog.txt")

        # ��·�������ļ��ж�ȡ��һ�μ�¼���ļ�
        if os.path.isfile(self.configFile):
            with open(self.configFile, "r") as f:
                count = 0
                for line in f.readlines():
                    count += 1
                    line = line.strip()
                    if count == 1:
                        self.textBoxSurfaceLibrary.Text = line
                    elif count == 2:
                        self.textBoxVolumeLibrary.Text = line
                    elif count == 3:
                        self.textBoxScDocxPath.Text = line
                    elif count == 4:
                        sim_type = line.split()[0]
                        self.radio_btn_cpu.Checked = (sim_type == "CPU")
                        self.radio_btn_gpu.Checked = (sim_type == "GPU")

        # ��ӿؼ�
        self.Controls.Add(self.labelSurfaceLibrary)
        self.Controls.Add(self.textBoxSurfaceLibrary)
        self.Controls.Add(self.btnChooseSurfacePath)
        self.Controls.Add(self.labelVolumeLibrary)
        self.Controls.Add(self.textBoxVolumeLibrary)
        self.Controls.Add(self.btnChooseVolumePath)
        self.Controls.Add(self.labelScDocxPath)
        self.Controls.Add(self.textBoxScDocxPath)
        self.Controls.Add(self.btnChooseScDocxPath)
        self.Controls.Add(self.btnCompute)
        self.Controls.Add(self.labelInfo)
        self.Controls.Add(self.groupBox)
        self.Controls.Add(self.label_pause)
        self.Controls.Add(self.checkbox_pause)
        self.groupBox.Controls.Add(self.radio_btn_cpu)
        self.groupBox.Controls.Add(self.radio_btn_gpu)
        
    def setSurfacePath(self, sender, event):
        dialog = FolderBrowserDialog()
        if dialog.ShowDialog() == DialogResult.OK:
            self.textBoxSurfaceLibrary.Text = dialog.SelectedPath

    def setVolumePath(self, sender, event):
        dialog = FolderBrowserDialog()
        if dialog.ShowDialog() == DialogResult.OK:
            self.textBoxVolumeLibrary.Text = dialog.SelectedPath
    
    def setScDocxPath(self, sender, event):
        dialog = OpenFileDialog()
        dialog.Filter = "scdocx files (*.scdocx)|*.scdocx"
        if dialog.ShowDialog() == DialogResult.OK:
            self.textBoxScDocxPath.Text = dialog.FileName
    
    def compute(self, sender, event):
        try: 
            self.labelInfo.Text = "��ʼִ�з���"
            self.computeAll()
        except Exception as e:
            self.handleError("ִ�з���ʱ��������", e)
    
    def computeAll(self):
        selectedSim = Selection.GetActive()
        if selectedSim == None or len(selectedSim.Items) != 1:
            MessageBox.Show("��ѡ��һ��simulation", "����", MessageBoxButtons.OK)
            return
        
        # д��·�������ļ�
        with open(self.configFile, "w") as f:
            f.write(self.textBoxSurfaceLibrary.Text + "\n")
            f.write(self.textBoxVolumeLibrary.Text + "\n")
            f.write(self.textBoxScDocxPath.Text + "\n")
            # д��CPU/GPU����
            if self.radio_btn_cpu.Checked:
                f.write(self.radio_btn_cpu.Text + " Compute" + "\n")
            else:
                f.write(self.radio_btn_gpu.Text + " Compute" + "\n")
        
        # ��������б�
        surfaceList = []
        if os.path.isdir(self.textBoxSurfaceLibrary.Text):
            surfaceList = getFiles(self.textBoxSurfaceLibrary.Text, [
                                    ".simplescattering",
                                    ".scattering",
                                    ".brdf",
                                    ".bsdf",
                                    ".bsdf180",
                                    ".coated",
                                    ".mirror",
                                    ".doe",
                                    ".fluorescent",
                                    ".grating",
                                    ".retroreflecting",
                                    ".anisotropic",
                                    ".polarizer",
                                    ".anisotropicbsdf",
                                    ".unpolished"
                                    ])
        else:
            print("δ���� Surface ·��!")
        
        # ��������б�
        volumeList = []
        if os.path.isdir(self.textBoxVolumeLibrary.Text):
            volumeList = getFiles(self.textBoxVolumeLibrary.Text, [
                                    ".material"])
        else:
            print("δ���� Volume ·��!")
        
        if len(surfaceList) == 0 and len(volumeList) == 0:
            MessageBox.Show("û���ҵ��κβ����ļ�������·���Ƿ���ȷ��", "����", MessageBoxButtons.OK)
            return
        
        if os.path.isfile(self.textBoxScDocxPath.Text) == False:
            MessageBox.Show("û���ҵ� scdocx �ļ�������·���Ƿ���ȷ��", "����", MessageBoxButtons.OK)
            return
        
        line = self.textBoxScDocxPath.Text
        baseName = os.path.basename(line)
        theDir = os.path.dirname(line)
        projectName = os.path.splitext(baseName)[0]
        self.outPath = os.path.join(theDir,"SPEOS output files", projectName)        
        
        try:
            material = SpeosSim.Material.Find("MAINMATERIAL")
        except Exception as e:
            self.handleError("δ�ҵ������쳣", e)
            MessageBox.Show("�뽫��������Ϊ��MAINMATERIAL", "����", MessageBoxButtons.OK)
            return
        
        self.computeSurface(selectedSim, material, surfaceList)
        self.computeVolume(selectedSim, material, volumeList)

        MessageBox.Show("ִ�н���!", "����", MessageBoxButtons.OK)
        self.labelInfo.Text = ""
    
    #
    def computeSurface(self, selectedSim, material, surfaceList = []):
        if len(surfaceList) == 0:
            return False
        
        if self.checkbox_pause.Checked and self.stop_sim == True:
            return False
        
        # ���� material ����
        material.VOPType = SpeosSim.Material.EnumVOPType.Opaque
        material.SOPType = SpeosSim.Material.EnumSOPType.Library
        
        for surfacePath in surfaceList:
            self.labelInfo.Text = "����ʹ�ã�" + surfacePath
            material.SOPLibrary = surfacePath

            if not self.compute_and_check(selectedSim):
                # ��ֹ����
                self.stop_sim = True
                break
            
            #SpeosSim.Command.ComputeOnActiveSelection()
            
            baseName = os.path.basename(surfacePath)
            imageName = os.path.splitext(baseName)[0] + ".png"
            surfaceDir = os.path.dirname(surfacePath)
            fullImageName = os.path.join(surfaceDir, imageName)            
                    
            # ����ͼƬ
            if self.exportImage(fullImageName) == False:
                self.labelInfo.Text = "����ͼƬʧ��:" + fullImageName
                return False
                
        return True
    
    #     
    def computeVolume(self, selectedSim, material, volumeList = []):
        if len(volumeList) == 0:
            return False
         
        if self.checkbox_pause.Checked and self.stop_sim == True:
            return False
        
        # ���� material ����
        material.VOPType = SpeosSim.Material.EnumVOPType.Library
        material.SOPType = SpeosSim.Material.EnumSOPType.OpticalPolished
        
        for volumePath in volumeList:
            self.labelInfo.Text = "����ʹ�ã�" + volumePath
            material.VOPLibrary = volumePath
            
            if not self.compute_and_check(selectedSim):
                # ��ֹ����
                self.stop_sim = True
                break
            
            #SpeosSim.Command.ComputeOnActiveSelection()
            
            baseName = os.path.basename(volumePath)
            imageName = os.path.splitext(baseName)[0] + ".png"
            volumeDir = os.path.dirname(volumePath)
            fullImageName = os.path.join(volumeDir, imageName)
            
            # ����ͼƬ
            if self.exportImage(fullImageName) == False:
                self.labelInfo.Text = "����ͼƬʧ��:" + fullImageName
                return False
        return True

    def compute_and_check(self, selectedSim):
        # ִ�з���ǰ����ɾ��Ŀ¼�е�xmp�ļ��������ڣ�
        if self.checkbox_pause.Checked:
            try:
                if Directory.Exists(self.outPath):
                    files = Directory.GetFiles(self.outPath)
                    for file_path in files:
                        try:
                            File.Delete(file_path)
                        except Exception as e:
                            print("�޷�ɾ���ļ� {0}: {1}".format(str(file_path), str(e)))
                else:
                    print("Ŀ¼ {0} ������".format(str(self.outPath)))
            except Exception as e:
                self.handleError("ɾ��xmp�ļ�����", e)

        # ִ�� ����
        if self.radio_btn_cpu.Checked:
            SpeosSim.Command.Compute(selectedSim.Items)
        else:
            SpeosSim.Command.GpuCompute(selectedSim.Items)
        print("�������")

        # ִ�з������Ŀ��Ŀ¼�в�����xmp�ļ�
        # �����ѡ ���ִ����Զ���ֹ
        if self.checkbox_pause.Checked:
            if Directory.Exists(self.outPath):
                files = Directory.GetFiles(self.outPath, "*.xmp")
                if not files:
                    print("��Ŀ¼ {0} ��û���ҵ��� .xmp Ϊ��׺���ļ���".format(str(self.outPath)))
                    return False
            else:
                print("Ŀ¼ {0} ������".format(str(self.outPath)))
                return False

        return True

    def exportImage(self, imageName):
        theFile =""
        for file in os.listdir(self.outPath):
            if file.endswith(".xmp"):
                theFile = os.path.join(self.outPath, file)
                break
        if theFile == "":
            print("û���ҵ� xmp �ļ�������·���Ƿ���ȷ�� '" + theFile + "'")
            #MessageBox.Show("û���ҵ� xmp �ļ�������·���Ƿ���ȷ��", "����", MessageBoxButtons.OK)
            return False
        
        self.labelInfo.Text = "���ڵ�����" + imageName
        print("����ͼƬ: '" + imageName + "'")
        
        # ʹ��Virtual Huamn Vision Lab�����ɵ�xmp
        try:
            if self.XmpViewer.OpenFile(theFile) != 1:
                print("XmpViewer ���ļ�ʧ�ܣ�" )
                return False
        except Exception as e:
            self.handleError("��ʹ��Virtual Huamn Vision Lab���ļ�ʱ�����쳣", e)
        
        # ��һ������Ϊ �����ͼƬ���ļ���
        # �ڶ�������Ϊ ͼ�θ�ʽ(0: BMP, 1: PNG, 2 :TIFF, 3: JPG)
        if self.XmpViewer.ExportXMPImage(imageName, 1) == 0:
            print("����ͼƬʧ��! '" + imageName + "'")
            #MessageBox.Show("����ͼƬʧ��", "����", MessageBoxButtons.OK)
            return False
        print("����ͼƬ�ɹ�!")
        return True
    
    # ������
    def handleError(self, message, exception):
        error_message = "{0}\n\n�������飺{1}".format(message, str(exception))
        MessageBox.Show(error_message, "����", MessageBoxButtons.OK)
        self.labelInfo.Text = error_message
        # ��¼��־
        log_file_path = self.errorlogFile
        # д����־�ļ�
        with open(log_file_path, "w") as f:
            f.write("{0}\n{1}\n\n".format(message, traceback.format_exc()))

    
def getFiles(path, suffixs = []):
    fileList = []
    
    if len(suffixs) == 0:
        for root, dirs, files in os.walk(path):
            for file in files:
                fileList.append(os.path.join(root, file))
    else:
        for root, dirs, files in os.walk(path):
            for file in files:
                suffix = os.path.splitext(file)[1].lower()
                
                if suffix not in suffixs: 
                    continue
                
                fileList.append(os.path.join(root, file))

    return fileList


def main():
    try:
        app = MainForm()
        
        # ��ģ̬
        app.Show()
        # ģ̬
        #app.ShowDialog()
    except Exception as e:
        print(e.ToString())

main()
