# Dibujado 2.5D

## Description

This program draws and allows you to rotate simple 3D models (like a tower or pyramid) in a 2.5D view based on axonometric projection.
It uses Pillow for wireframe rendering and CustomTkinter as the interactive graphical interface.

You can rotate the model with the mouse and zoom with the scroll wheel.
The drawing system doesn't use a true 3D engine, but rather mathematical transformations that project 3D points onto a 2D plane, achieving a fluid and lightweight three-dimensional effect.

Furthermore, it supports loading external models from .txt files (generated or converted from .obj), allowing you to visualize custom structures without modifying the main code.

### Dependencies & Requerements

* Python: >= v3.10
* customtkinter v25.3

## Authors

ex. Raúl Arath León López - C22760499
ex. [ZeusLeon](https://github.com/ZeusLeon2002)

## Version History
* 0.1
    * Initial Release: The code is capable of transforming an .obj model into a readable .txt file to draw the vertices and edges on the screen.
