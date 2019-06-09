import cv2
import numpy as np


class HandShape:
    def __init__(self, shape, msg):
        self.shape = shape
        self.msg = msg
        self.count = 0

    def reset_count(self):
        self.count = 0

    def inc_count(self):
        self.count += 1


show_detailed = False
color_keying = False
five_fingers = np.matrix(
    [[74, 0], [73, 1], [72, 1], [71, 2], [70, 2], [70, 4], [69, 5], [68, 5], [68, 8], [67, 9], [66, 9], [66, 10],
     [68, 12], [68, 20], [69, 20], [70, 21], [70, 22], [69, 23], [68, 22], [68, 25], [69, 24], [70, 25], [70, 32],
     [69, 33], [70, 34], [70, 39], [69, 40], [70, 41], [70, 51], [69, 52], [68, 52], [68, 62], [69, 62], [70, 63],
     [69, 64], [68, 64], [68, 66], [69, 67], [68, 68], [68, 85], [67, 86], [68, 87], [68, 91], [67, 92], [68, 93],
     [68, 95], [67, 96], [67, 97], [66, 98], [65, 98], [65, 99], [64, 100], [63, 99], [63, 98], [62, 98], [61, 97],
     [61, 94], [63, 92], [62, 92], [61, 91], [61, 85], [60, 86], [59, 85], [59, 78], [58, 79], [57, 78], [57, 76],
     [58, 75], [59, 75], [59, 74], [56, 74], [55, 73], [57, 71], [57, 68], [56, 67], [56, 63], [55, 62], [55, 60],
     [54, 60], [53, 59], [54, 58], [55, 58], [54, 58], [53, 57], [53, 48], [52, 48], [51, 47], [51, 42], [52, 41],
     [51, 40], [51, 37], [49, 35], [49, 33], [50, 32], [51, 33], [51, 32], [49, 30], [49, 26], [48, 25], [49, 24],
     [48, 24], [47, 23], [47, 20], [46, 19], [44, 19], [43, 18], [43, 17], [42, 18], [41, 17], [36, 17], [35, 18],
     [34, 18], [30, 22], [30, 23], [28, 25], [28, 32], [29, 33], [28, 34], [28, 36], [29, 37], [29, 42], [28, 43],
     [28, 44], [29, 44], [30, 45], [30, 48], [31, 49], [30, 50], [30, 51], [32, 53], [32, 54], [31, 55], [32, 56],
     [33, 56], [34, 57], [33, 58], [32, 58], [33, 58], [34, 59], [33, 60], [34, 61], [34, 72], [35, 72], [36, 73],
     [35, 74], [34, 74], [34, 75], [35, 75], [36, 76], [36, 77], [35, 78], [34, 77], [34, 78], [35, 78], [36, 79],
     [36, 82], [37, 82], [38, 83], [38, 85], [37, 86], [37, 88], [36, 89], [37, 89], [38, 90], [38, 94], [40, 96],
     [39, 97], [38, 97], [38, 98], [39, 98], [40, 99], [40, 105], [41, 105], [42, 106], [42, 114], [41, 115], [38, 115],
     [37, 114], [37, 112], [36, 112], [35, 111], [35, 110], [34, 109], [35, 108], [34, 109], [33, 108], [33, 106],
     [32, 106], [31, 105], [30, 105], [29, 104], [30, 103], [28, 101], [28, 99], [27, 98], [27, 92], [26, 92], [25, 91],
     [25, 87], [23, 85], [23, 77], [23, 78], [22, 79], [21, 78], [21, 69], [19, 67], [19, 64], [18, 63], [18, 61],
     [16, 59], [16, 58], [15, 57], [15, 55], [13, 53], [11, 53], [9, 51], [8, 51], [7, 52], [5, 52], [4, 53], [3, 53],
     [4, 54], [2, 56], [2, 57], [1, 58], [1, 60], [0, 61], [0, 64], [1, 65], [0, 66], [1, 67], [1, 68], [2, 69],
     [0, 71], [0, 72], [2, 74], [2, 78], [3, 79], [2, 80], [4, 82], [4, 86], [5, 87], [5, 89], [6, 90], [6, 93],
     [7, 94], [7, 98], [8, 99], [8, 101], [9, 102], [9, 104], [10, 105], [10, 108], [12, 110], [11, 111], [12, 112],
     [12, 113], [16, 117], [15, 118], [16, 119], [16, 125], [17, 125], [18, 126], [18, 132], [19, 132], [20, 133],
     [20, 134], [19, 135], [18, 135], [19, 135], [20, 136], [20, 142], [21, 142], [22, 143], [22, 162], [23, 162],
     [24, 163], [23, 164], [22, 164], [22, 166], [23, 166], [24, 167], [24, 168], [23, 169], [22, 169], [22, 172],
     [23, 172], [24, 173], [24, 190], [25, 191], [25, 192], [26, 193], [26, 196], [27, 196], [28, 197], [28, 202],
     [29, 203], [29, 205], [30, 206], [30, 208], [31, 209], [30, 210], [30, 211], [31, 212], [31, 213], [32, 214],
     [31, 215], [31, 217], [32, 218], [32, 219], [31, 220], [31, 222], [32, 223], [32, 225], [31, 226], [32, 227],
     [32, 228], [31, 229], [31, 235], [30, 236], [30, 240], [29, 241], [28, 241], [29, 241], [30, 242], [30, 243],
     [29, 244], [29, 246], [28, 247], [28, 250], [100, 250], [100, 249], [102, 247], [102, 246], [103, 245], [103, 241],
     [104, 240], [105, 240], [105, 238], [104, 238], [103, 237], [106, 234], [105, 233], [106, 232], [107, 232],
     [109, 230], [109, 229], [110, 228], [113, 228], [114, 227], [113, 226], [114, 225], [116, 225], [117, 226],
     [117, 225], [118, 224], [119, 224], [119, 223], [121, 221], [122, 222], [124, 220], [125, 220], [127, 218],
     [127, 217], [128, 216], [130, 216], [132, 214], [133, 214], [133, 213], [137, 209], [138, 210], [139, 210],
     [139, 209], [142, 206], [141, 205], [142, 204], [144, 204], [145, 205], [145, 203], [146, 202], [147, 202],
     [147, 201], [148, 200], [151, 200], [151, 197], [153, 195], [155, 195], [157, 193], [157, 192], [158, 191],
     [158, 190], [159, 189], [161, 189], [161, 188], [163, 186], [165, 186], [165, 185], [166, 184], [167, 184],
     [167, 182], [168, 181], [168, 180], [169, 179], [170, 179], [171, 178], [171, 177], [172, 176], [173, 176],
     [173, 174], [175, 172], [175, 171], [177, 169], [178, 169], [178, 168], [179, 167], [180, 168], [180, 166],
     [179, 165], [180, 164], [183, 164], [183, 163], [186, 160], [187, 160], [189, 158], [190, 158], [191, 157],
     [191, 155], [192, 154], [195, 154], [195, 152], [197, 150], [197, 149], [198, 148], [198, 147], [199, 146],
     [200, 147], [201, 147], [201, 146], [202, 145], [202, 144], [203, 143], [204, 143], [203, 142], [203, 141],
     [208, 136], [210, 136], [211, 135], [211, 134], [212, 133], [213, 133], [215, 131], [215, 125], [214, 125],
     [213, 124], [213, 123], [212, 122], [211, 123], [209, 121], [208, 121], [207, 120], [204, 120], [203, 119],
     [203, 118], [202, 118], [201, 119], [196, 119], [195, 120], [192, 120], [192, 121], [191, 122], [188, 122],
     [187, 123], [186, 123], [185, 124], [182, 124], [182, 126], [181, 127], [180, 127], [179, 128], [178, 127],
     [178, 126], [178, 128], [177, 129], [176, 129], [176, 131], [175, 132], [172, 132], [172, 134], [171, 135],
     [170, 135], [170, 137], [169, 138], [168, 138], [168, 139], [167, 140], [164, 140], [164, 141], [163, 142],
     [162, 142], [148, 156], [145, 156], [144, 157], [143, 156], [143, 155], [140, 155], [139, 156], [138, 156],
     [137, 155], [135, 155], [133, 153], [132, 153], [130, 151], [129, 151], [128, 150], [128, 149], [127, 148],
     [127, 146], [126, 145], [126, 144], [125, 143], [125, 141], [126, 140], [126, 139], [125, 138], [125, 137],
     [123, 135], [123, 134], [124, 133], [125, 133], [125, 131], [126, 130], [127, 130], [126, 130], [125, 129],
     [124, 129], [123, 128], [123, 123], [124, 122], [125, 122], [125, 121], [124, 122], [123, 121], [123, 120],
     [124, 119], [125, 119], [125, 98], [126, 97], [125, 96], [125, 95], [126, 94], [126, 93], [127, 92], [127, 80],
     [128, 79], [129, 80], [129, 73], [130, 72], [130, 71], [129, 70], [129, 64], [130, 63], [131, 63], [131, 50],
     [130, 50], [129, 49], [130, 48], [131, 48], [131, 44], [132, 43], [131, 42], [131, 40], [130, 41], [129, 40],
     [129, 39], [130, 38], [131, 38], [131, 30], [130, 31], [129, 30], [129, 28], [131, 26], [131, 24], [129, 22],
     [129, 18], [128, 18], [127, 17], [127, 13], [126, 13], [125, 12], [125, 10], [122, 10], [121, 9], [118, 9],
     [117, 8], [117, 7], [116, 7], [117, 8], [116, 9], [112, 9], [109, 12], [108, 12], [108, 13], [107, 14], [106, 14],
     [106, 15], [107, 14], [108, 15], [108, 21], [107, 22], [106, 22], [106, 24], [107, 24], [108, 25], [107, 26],
     [106, 26], [106, 32], [105, 33], [106, 34], [106, 37], [105, 38], [106, 39], [106, 46], [107, 46], [108, 47],
     [108, 49], [107, 50], [106, 50], [106, 60], [105, 61], [104, 61], [104, 65], [103, 66], [102, 66], [102, 76],
     [101, 77], [100, 77], [100, 86], [98, 88], [98, 94], [97, 95], [96, 95], [96, 96], [95, 97], [92, 97], [91, 96],
     [92, 95], [91, 94], [91, 91], [93, 89], [92, 89], [91, 88], [92, 87], [92, 86], [91, 85], [91, 83], [92, 82],
     [93, 82], [93, 76], [92, 76], [91, 75], [91, 73], [92, 72], [93, 72], [93, 71], [91, 69], [91, 68], [93, 66],
     [93, 62], [92, 62], [91, 61], [91, 59], [92, 58], [93, 58], [93, 56], [94, 55], [95, 55], [94, 55], [93, 54],
     [93, 53], [91, 51], [92, 50], [92, 48], [91, 47], [91, 42], [92, 41], [93, 41], [91, 39], [91, 33], [92, 32],
     [92, 30], [91, 29], [91, 22], [90, 21], [90, 20], [91, 19], [91, 15], [90, 14], [91, 13], [91, 12], [90, 12],
     [89, 11], [89, 9], [88, 8], [88, 7], [87, 6], [87, 3], [85, 3], [83, 1], [76, 1], [75, 0]])
fist_with_finger = np.matrix(
    [[96, 0], [96, 1], [95, 2], [93, 2], [92, 3], [92, 4], [91, 5], [88, 5], [89, 6], [89, 7], [88, 8], [87, 7],
     [85, 7], [83, 5], [72, 5], [72, 6], [69, 9], [68, 9], [67, 10], [67, 11], [65, 13], [64, 13], [63, 12], [62, 12],
     [61, 11], [61, 10], [55, 10], [53, 12], [49, 12], [48, 13], [47, 13], [46, 14], [46, 15], [43, 18], [43, 19],
     [41, 21], [40, 21], [39, 20], [38, 20], [37, 21], [36, 20], [32, 20], [31, 21], [30, 21], [29, 22], [28, 22],
     [27, 23], [25, 23], [25, 24], [24, 25], [24, 26], [23, 27], [22, 27], [21, 28], [20, 28], [20, 29], [18, 31],
     [18, 33], [17, 34], [16, 34], [16, 40], [14, 42], [14, 44], [13, 45], [13, 47], [11, 49], [12, 50], [12, 57],
     [11, 58], [11, 59], [10, 60], [10, 61], [11, 62], [11, 70], [10, 71], [10, 72], [11, 73], [10, 74], [10, 75],
     [9, 76], [10, 77], [10, 78], [9, 79], [8, 79], [10, 81], [9, 82], [10, 83], [10, 85], [9, 86], [10, 87], [10, 93],
     [11, 93], [12, 94], [12, 95], [11, 96], [11, 97], [12, 96], [13, 97], [13, 100], [12, 101], [12, 102], [13, 101],
     [14, 102], [14, 103], [13, 104], [12, 104], [12, 107], [12, 105], [13, 104], [14, 105], [14, 108], [15, 109],
     [15, 115], [14, 116], [15, 117], [15, 144], [14, 145], [13, 144], [12, 144], [12, 146], [13, 145], [14, 146],
     [14, 147], [13, 148], [13, 150], [12, 151], [13, 152], [12, 153], [12, 158], [11, 159], [11, 163], [9, 165],
     [8, 165], [9, 165], [10, 166], [10, 167], [9, 168], [9, 172], [6, 175], [6, 177], [5, 178], [6, 178], [7, 179],
     [7, 181], [6, 182], [6, 184], [4, 186], [4, 191], [3, 192], [2, 191], [2, 199], [1, 200], [0, 199], [0, 200],
     [73, 200], [73, 198], [74, 197], [75, 197], [74, 196], [74, 192], [75, 191], [75, 187], [74, 186], [74, 184],
     [75, 183], [76, 184], [76, 183], [77, 182], [77, 176], [76, 175], [76, 174], [77, 173], [77, 168], [78, 167],
     [79, 168], [79, 171], [79, 168], [80, 167], [78, 165], [79, 164], [81, 164], [81, 163], [80, 162], [79, 162],
     [78, 161], [81, 158], [81, 155], [83, 153], [83, 150], [82, 150], [81, 149], [82, 148], [83, 148], [83, 145],
     [84, 144], [84, 142], [85, 141], [85, 139], [87, 137], [87, 133], [88, 132], [88, 131], [90, 129], [91, 129],
     [91, 126], [92, 125], [92, 124], [93, 123], [94, 124], [94, 125], [95, 124], [95, 121], [96, 120], [97, 120],
     [98, 121], [100, 119], [103, 119], [105, 117], [107, 117], [107, 115], [108, 114], [109, 114], [110, 115],
     [111, 115], [111, 114], [112, 113], [113, 113], [116, 110], [115, 109], [116, 108], [118, 108], [120, 106],
     [121, 106], [121, 105], [122, 104], [123, 105], [123, 104], [124, 103], [125, 103], [130, 98], [131, 98],
     [132, 97], [133, 97], [134, 96], [135, 96], [135, 95], [136, 94], [137, 94], [137, 93], [138, 92], [140, 92],
     [141, 91], [143, 91], [143, 89], [144, 88], [145, 89], [145, 88], [147, 86], [149, 86], [149, 84], [150, 83],
     [151, 83], [152, 82], [153, 82], [153, 81], [154, 80], [155, 80], [155, 79], [157, 77], [157, 76], [158, 75],
     [159, 75], [160, 74], [161, 74], [160, 74], [159, 75], [158, 74], [158, 73], [159, 72], [160, 72], [159, 71],
     [161, 69], [162, 69], [161, 68], [162, 67], [163, 67], [164, 66], [165, 66], [165, 64], [164, 64], [163, 63],
     [163, 62], [164, 61], [165, 61], [166, 62], [167, 62], [167, 61], [166, 60], [167, 59], [171, 59], [171, 58],
     [172, 57], [173, 57], [173, 56], [174, 55], [177, 55], [177, 53], [178, 52], [179, 52], [179, 50], [180, 49],
     [181, 49], [181, 47], [182, 46], [183, 46], [182, 46], [181, 45], [181, 42], [182, 41], [185, 41], [186, 40],
     [187, 40], [187, 39], [188, 38], [189, 38], [190, 37], [191, 37], [191, 36], [192, 35], [195, 35], [198, 32],
     [199, 33], [199, 32], [200, 31], [202, 31], [203, 30], [202, 30], [201, 29], [202, 28], [203, 28], [203, 27],
     [201, 25], [200, 25], [199, 24], [198, 24], [197, 23], [197, 22], [196, 23], [194, 23], [193, 22], [183, 22],
     [182, 23], [181, 23], [180, 24], [179, 23], [178, 23], [177, 24], [175, 24], [171, 28], [169, 28], [167, 30],
     [166, 30], [166, 31], [165, 32], [164, 32], [163, 33], [162, 33], [161, 34], [160, 34], [160, 35], [159, 36],
     [158, 36], [158, 39], [157, 40], [156, 39], [156, 40], [155, 41], [154, 41], [153, 42], [152, 42], [152, 43],
     [151, 44], [150, 44], [150, 45], [149, 46], [148, 46], [148, 48], [147, 49], [144, 49], [144, 50], [143, 51],
     [142, 50], [142, 51], [141, 52], [140, 52], [140, 53], [139, 54], [138, 54], [137, 55], [136, 54], [135, 55],
     [134, 55], [134, 57], [133, 58], [132, 57], [131, 57], [130, 58], [129, 57], [128, 57], [127, 58], [126, 58],
     [125, 57], [124, 58], [123, 57], [123, 56], [121, 54], [121, 46], [120, 46], [119, 45], [119, 43], [120, 42],
     [119, 41], [119, 38], [120, 37], [120, 36], [119, 35], [119, 28], [118, 28], [117, 27], [118, 26], [120, 26],
     [120, 24], [119, 23], [119, 13], [118, 13], [117, 12], [117, 10], [116, 10], [115, 9], [115, 8], [114, 8],
     [113, 7], [113, 6], [112, 5], [111, 5], [108, 2], [107, 2], [106, 1], [105, 2], [103, 0], [102, 1], [101, 1],
     [100, 0], [99, 1], [97, 1]])
five_fingers_shape = HandShape(five_fingers, 'Five Fingers')
fist_with_finger_shape = HandShape(fist_with_finger, 'Pointing')
shapes = [five_fingers_shape, fist_with_finger_shape]
minimal_count = 5000


class GestureHandler:
    def __init__(self, cam_num):
        self.cam_num = cam_num

        self.x_center, self.y_center = None, None
        self.x_counter, self.y_counter = 0, 0
        global shapes
        self.cap = cv2.VideoCapture(self.cam_num)

        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)

    def update(self):
        ret, img = self.cap.read()

        preprocessed = None

        if color_keying:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, (4, 15, 100), (70, 170, 255))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask2 = cv2.inRange(hsv, (140, 0, 50), (165, 160, 255))

            if show_detailed:
                cv2.imshow("1", mask)
                cv2.imshow("2", mask2)

            imask = mask + mask2 > 0
            skin = np.zeros_like(img, np.uint8)
            skin[imask] = img[imask]
            preprocessed = skin
        else:
            preprocessed = img

        fg_mask = self.fgbg.apply(preprocessed)

        whites_count = cv2.countNonZero(fg_mask)

        blur = cv2.GaussianBlur(fg_mask, (11, 11), 0)
        _, gaussian = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        if show_detailed:
            cv2.imshow("gaussian", gaussian)

        contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        max_area = 0
        ci = None
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                ci = i
        if ci is not None:
            cnt = contours[ci]

        hull = cv2.convexHull(cnt)

        x, y, w, h = cv2.boundingRect(cnt)

        cropped_gaussian = gaussian[y:y + h, x:x + w]
        if show_detailed:
            cv2.imshow("crop", cropped_gaussian)

        drawing = np.zeros(img.shape, np.uint8)
        if whites_count > minimal_count:
            cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 2)
            cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 2)
            cv2.drawContours(img, [cnt], 0, (0, 255, 0), 2)
            cv2.drawContours(img, [hull], 0, (0, 0, 255), 2)

        x_previous = self.x_center
        y_previous = self.y_center

        x_center = 0
        y_center = 0
        for i in hull:
            x_center += i[0][0]
            y_center += i[0][1]

        x_center /= len(hull)
        y_center /= len(hull)

        if x_previous is not None and y_previous is not None and whites_count > minimal_count:
            x_delta = (x_center - x_previous)
            y_delta = (y_center - y_previous)
        else:
            for s in shapes:
                s.reset_count()
            x_delta = 0
            y_delta = 0

        if whites_count < minimal_count:
            for s in shapes:
                s.reset_count()
            x_counter = 0
            y_counter = 0
        else:
            self.x_counter += x_delta
            self.y_counter += y_delta

        hull = cv2.convexHull(cnt)

        if whites_count > minimal_count and x_previous is not None and y_previous is not None:
            cv2.drawMarker(drawing, (int(x_center), int(y_center)), (255, 0, 255))
            cv2.drawMarker(drawing, (int(x_previous), int(y_previous)), (255, 255, 255))
            cv2.drawMarker(img, (int(x_center), int(y_center)), (255, 0, 255))
            cv2.drawMarker(img, (int(x_previous), int(y_previous)), (255, 255, 255))

        contour_gaussian_cropped = np.matrix(list(map(lambda a: [a[0][0] - x, a[0][1] - y], cnt)))

        rets = [cv2.matchShapes(x.shape, contour_gaussian_cropped, 1, 0.0) for x in shapes]

        m_ret = 1
        m_sh = None

        for i, sh in zip(rets, shapes):
            if m_ret > i:
                m_ret = i
                m_sh = sh

        if whites_count > minimal_count and m_ret < 0.1:
            m_sh.inc_count()

        if self.x_counter > 400:
            tmp_m_sh = None
            tmp_m_count = -1
            for s in shapes:
                if tmp_m_count < s.count:
                    tmp_m_count = s.count
                    tmp_m_sh = s
            if tmp_m_sh.count > 5:
                print(tmp_m_sh.msg + ' left ' + str(tmp_m_sh.count))

        if self.x_counter < -400:
            tmp_m_sh = None
            tmp_m_count = -1
            for s in shapes:
                if tmp_m_count < s.count:
                    tmp_m_count = s.count
                    tmp_m_sh = s
            if tmp_m_sh.count > 5:
                print(tmp_m_sh.msg + ' right ' + str(tmp_m_sh.count))

        if color_keying:
            cv2.imshow('skin', skin)

        if show_detailed:
            cv2.imshow('fg_mask', fg_mask)
            cv2.imshow('drawing', drawing)
        cv2.imshow('img', img)

        k = cv2.waitKey(10)
        if k == 27:
            exit(0)
        if k == 32:
            tmp_m_sh = None
            tmp_m_count = -1
            for s in shapes:
                if tmp_m_count < s.count:
                    tmp_m_count = s.count
                    tmp_m_sh = s
            print(tmp_m_sh.msg)
            print(whites_count)
        if k == 114:
            fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)
