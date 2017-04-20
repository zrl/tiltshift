# Final Project
# Zachary Levin

import cv2


class Image:
    n_kern = 19
    kernels = [1 + (4 * x) for x in range(n_kern)]
    kernels.sort(reverse=True)
    dimension_string = '{}x{}'

    def __init__(self, filename):
        self.image_array = cv2.imread(filename)
        self.color = 3 == len(self.image_array.shape)
        self.height = self.image_array.shape[0]
        self.width = self.image_array.shape[1]
        self.linear_center = self.height // 2
        self.tiltshift_radius = self.height // 50
        self.top_split = []
        self.bottom_split = []
        self.center = ()

    def write(self, filename):
        cv2.imwrite(filename, self.image_array)

    def dimensions(self):
        return Image.dimension_string.format(int(self.height), int(self.width))

    def check(self):
        if not 0 <= self.linear_center <= self.height:
            self.linear_center = self.height // 2
        if not 0 <= self.tiltshift_radius <= self.height:
            self.tiltshift_radius = self.height // 50

    def define_center(self):
        top = self.linear_center - self.tiltshift_radius
        bottom = self.linear_center + self.tiltshift_radius

        top = 0 if top < 0 else top
        bottom = self.height if bottom > self.height else bottom
        self.center = (top, bottom)

    def define_blur_ranges(self):
        top_width = self.center[0]
        bottom_width = self.height - self.center[1]

        if top_width > bottom_width:
            blur_width = top_width // Image.n_kern
            ttop_split = [blur_width * x for x in range(len(Image.kernels) + 1)]
            tbottom_split = [self.center[1]]

            while tbottom_split[-1] + 2 * blur_width < self.height:
                tbottom_split.append(tbottom_split[-1] + blur_width)
            tbottom_split.append(self.height)

        else:
            blur_width = bottom_width // Image.n_kern
            tbottom_split = [self.center[1] + (blur_width * x) for x in range(len(Image.kernels))]
            tbottom_split.append(self.height)
            ttop_split = [self.center[0]]

            while ttop_split[-1] - 2 * blur_width > 0:
                ttop_split.append(ttop_split[-1] - blur_width)
            ttop_split.append(0)

        ttop_split.sort()
        tbottom_split.sort(reverse=True)

        self.top_split = ttop_split
        self.bottom_split = tbottom_split

    def apply_blur(self):
        for i in range(len(Image.kernels)):
            curr_k_size = Image.kernels[i]
            current_kernel = (curr_k_size, curr_k_size)

            if i + 1 < len(self.top_split):
                NT = curr_k_size if i - curr_k_size >= 0 else 0
                NB = curr_k_size
                self.image_array[self.top_split[i]:self.top_split[i + 1]] = \
                    cv2.blur(self.image_array[self.top_split[i] - NT:self.top_split[i + 1] + NB], current_kernel,
                             borderType=cv2.BORDER_REFLECT_101)[NT:abs(self.top_split[i + 1] - self.top_split[i]) + NT]

            if i + 1 < len(self.bottom_split):
                MT = curr_k_size
                MB = curr_k_size if i + curr_k_size <= self.height else 0
                self.image_array[self.bottom_split[i + 1]:self.bottom_split[i]] = \
                    cv2.blur(self.image_array[self.bottom_split[i + 1] - MT:self.bottom_split[i] + MB], current_kernel,
                             borderType=cv2.BORDER_REFLECT_101)[
                    MT:abs(self.bottom_split[i] - self.bottom_split[i + 1]) + MT]

    def smooth_blur(self):
        self.image_array[:self.center[0]] = cv2.GaussianBlur(self.image_array[:self.center[0]], (5, 5), sigmaX=1,
                                                             sigmaY=5,
                                                             borderType=cv2.BORDER_REFLECT_101)
        self.image_array[self.center[1]:] = cv2.GaussianBlur(self.image_array[self.center[1]:], (5, 5), sigmaX=1,
                                                             sigmaY=5,
                                                             borderType=cv2.BORDER_REFLECT_101)

    def tiltshift(self):
        self.check()
        self.define_center()
        self.define_blur_ranges()
        self.apply_blur()
        self.smooth_blur()
