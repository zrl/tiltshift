# Miniature Faking with Tilt-shift Post-Processing
## OMSCS 6475 - Spring 2017

### Project Description

This script is used during post-processing to simulate [tilt-shift photography](https://en.wikipedia.org/wiki/Tilt–shift_photography). The result is known as [miniature faking](https://en.wikipedia.org/wiki/Miniature_faking). The script applies a linear blur gradient to achieve this effect.

### Usage
1. Place images to be edited in the `source` folder.
2. Run `python tiltshift.py`
3. For each image, the script will prompt to input the center of the area to remain in focus and the radius of the focal area

### Primary Reference

Held, R. T., Cooper, E. A., O’Brien, J. F., and Banks, M. S. 2010. Using Blur to Affect Perceived Distance and Size. ACM Trans. Graph. 29, 2, Article 19 (March 2010), 16 pages. DOI = 10.1145/1731047.1731057 [http://doi.acm.org/10.1145/1731047.1731057](http://doi.acm.org/10.1145/1731047.1731057)

---
&copy; 2017 [Zachary Levin](mailto:code@zrlevin.com)