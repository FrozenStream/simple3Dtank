

def read_mtl(mtl_source):
    mtl_project = open(mtl_source, 'r')
    glo_dic = {}
    dic = {}
    mtl_name = None
    for line in mtl_project:
        single_line = line.split()
        if not single_line or single_line[0] == '#':
            continue
        if single_line[0] == 'newmtl':
            if mtl_name:
                glo_dic[mtl_name] = dic.copy()
            mtl_name = single_line[1]
            dic.clear()
        # 获取mtl材质名
        if single_line[0] == 'Ns':
            dic['Ns'] = float(single_line[1])
        if single_line[0] == 'd':
            dic['d'] = float(single_line[1])
        if single_line[0] == 'Tr':
            dic['Tr'] = float(single_line[1])
        if single_line[0] == 'Tf':
            dic['Tf'] = float(single_line[1])
        if single_line[0] == 'illum':
            dic['illum'] = float(single_line[1])
        if single_line[0] == 'Ka':
            dic['Ka'] = [float(x) for x in single_line[1:4]]
        if single_line[0] == 'Kd':
            dic['Kd'] = [float(x) for x in single_line[1:4]]
        if single_line[0] == 'Ks':
            dic['Ks'] = [float(x) for x in single_line[1:4]]
    if mtl_name:
        glo_dic[mtl_name] = dic
    mtl_project.close()
    return glo_dic


class ObjLoad1:
    def __init__(self, obj_source):
        self.points_v = []
        self.points_vn = []
        self.points_vt = []
        self.face = []
        self.mtl_dic = {}
        self.pre_mtl = None
        obj_project = open(obj_source, 'r')
        for line in obj_project:
            single_line = line.split()
            if len(single_line) < 2:
                continue

            if single_line[0] == 'mtllib':
                self.mtl_dic.update(read_mtl('./models/'+single_line[1]))
            # 读取.mtl文件
            if single_line[0] == 'v':
                self.points_v.append([float(x) for x in single_line[1:4]])
            # 读取点坐标(x,y,z)
            if single_line[0] == 'vn':
                self.points_vn.append([float(x) for x in single_line[1:4]])
            # 读取点法向量(x,y,z)
            if single_line[0] == 'vt':
                self.points_vt.append([float(x) for x in single_line[1:4]])
            # 读取点纹理坐标(x,y,z)
            if single_line[0] == 'usemtl':
                self.pre_mtl = single_line[1]
            # 获取材质名
            if single_line[0] == 'f':
                vertex1 = single_line[1].split('/')
                vertex1 = [int(x) for x in vertex1]
                vertex2 = single_line[2].split('/')
                vertex2 = [int(x) for x in vertex2]
                vertex3 = single_line[3].split('/')
                vertex3 = [int(x) for x in vertex3]
                self.face.append([self.pre_mtl, vertex1.copy(), vertex2.copy(), vertex3.copy()])
        obj_project.close()


class ObjLoad2:
    def __init__(self, obj_source):
        self.points_v = []
        self.points_vn = []
        self.points_vt = []
        self.face = []
        self.mtl_dic = {}
        self.pre_mtl = None
        obj_project = open(obj_source, 'r')
        for line in obj_project:
            single_line = line.split()
            if len(single_line) < 2:
                continue

            if single_line[0] == 'mtllib':
                self.mtl_dic.update(read_mtl('./models/'+single_line[1]))
            # 读取.mtl文件
            if single_line[0] == 'v':
                self.points_v.append([float(x) for x in single_line[1:4]])
            # 读取点坐标(x,y,z)
            if single_line[0] == 'vn':
                self.points_vn.append([float(x) for x in single_line[1:4]])
            # 读取点法向量(x,y,z)
            if single_line[0] == 'vt':
                self.points_vt.append([float(x) for x in single_line[1:4]])
            # 读取点纹理坐标(x,y,z)
            if single_line[0] == 'usemtl':
                self.pre_mtl = single_line[1]
            # 获取材质名
            if single_line[0] == 'f':
                vertex1 = single_line[1].split('//')
                vertex1 = [int(x) for x in vertex1]
                vertex2 = single_line[2].split('//')
                vertex2 = [int(x) for x in vertex2]
                vertex3 = single_line[3].split('//')
                vertex3 = [int(x) for x in vertex3]
                self.face.append([self.pre_mtl, vertex1.copy(), vertex2.copy(), vertex3.copy()])
        obj_project.close()