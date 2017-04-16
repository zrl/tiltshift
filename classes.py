# Final Project
# Zachary Levin

import cv2
import numpy as np


def gen_top_filter(k):
    out_array = np.zeros((k, k))

    for i in range(k):
        out_array[i].fill(k - i)
    return out_array / out_array.sum()


def gen_bot_filter(k):
    out_array = np.zeros((k, k))

    for i in range(k):
        out_array[i].fill(i + 1)
    return out_array / out_array.sum()


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
        center = (top, bottom)
        return center

    def define_blur_ranges(self):
        center = self.define_center()
        top_width = center[0]
        bottom_width = self.height - center[1]

        if top_width > bottom_width:
            blur_width = top_width // Image.n_kern
            top_split = [blur_width * x for x in range(len(Image.kernels) + 1)]
            bottom_split = [center[1]]

            while bottom_split[-1] + 2 * blur_width < self.height:
                bottom_split.append(bottom_split[-1] + blur_width)
            bottom_split.append(self.height)

        else:
            blur_width = bottom_width // Image.n_kern
            bottom_split = [center[1] + (blur_width * x) for x in range(len(Image.kernels))]
            bottom_split.append(self.height)
            top_split = [center[0]]

            while top_split[-1] - 2 * blur_width > 0:
                top_split.append(top_split[-1] - blur_width)
            top_split.append(0)

        top_split.sort()
        bottom_split.sort(reverse=True)

        return top_split, bottom_split, center

    def tiltshift(self):
        self.check()

        top_split, bottom_split, center = self.define_blur_ranges()

        for i in range(len(Image.kernels)):
            curr_k_size = Image.kernels[i]
            current_kernel = (curr_k_size, curr_k_size)

            if i + 1 < len(top_split):
                NT = curr_k_size if i - curr_k_size >= 0 else 0
                NB = curr_k_size
                self.image_array[top_split[i]:top_split[i + 1]] = \
                    cv2.blur(self.image_array[top_split[i] - NT:top_split[i + 1] + NB], current_kernel,
                             borderType=cv2.BORDER_REFLECT_101)[NT:abs(top_split[i + 1] - top_split[i]) + NT]

            if i + 1 < len(bottom_split):
                MT = curr_k_size
                MB = curr_k_size if i + curr_k_size <= self.height else 0
                self.image_array[bottom_split[i + 1]:bottom_split[i]] = \
                    cv2.blur(self.image_array[bottom_split[i + 1] - MT:bottom_split[i] + MB], current_kernel,
                             borderType=cv2.BORDER_REFLECT_101)[MT:abs(bottom_split[i] - bottom_split[i + 1]) + MT]

        self.image_array[:center[0]] = cv2.GaussianBlur(self.image_array[:center[0]], (5, 5), sigmaX=1, sigmaY=5,
                                                        borderType=cv2.BORDER_REFLECT_101)
        self.image_array[center[1]:] = cv2.GaussianBlur(self.image_array[center[1]:], (5, 5), sigmaX=1, sigmaY=5,
                                                        borderType=cv2.BORDER_REFLECT_101)
