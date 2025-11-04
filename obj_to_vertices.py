import math

def convert_obj_a_modelo(obj_filename, output_filename, scale=0.1, rot_x=245):
    vertices = []
    edges = set()
    rad_x = math.radians(rot_x)

    with open(obj_filename, "r") as f:
        for line in f:
            parts = line.strip().split()
            if not parts or parts[0].startswith("#"):
                continue

            if parts[0] == "v":
                x, y, z = map(float, parts[1:])
                x *= scale
                y *= scale
                z *= scale

                y2 = y * math.cos(rad_x) - z * math.sin(rad_x)
                z2 = y * math.sin(rad_x) + z * math.cos(rad_x)
                vertices.append((x, y2, z2))

            elif parts[0] == "f":
                indices = [int(p.split("/")[0]) for p in parts[1:]]
                for i in range(len(indices)):
                    a = indices[i]
                    b = indices[(i + 1) % len(indices)]
                    edges.add(tuple(sorted((a, b))))

    with open(output_filename, "w") as out:
        for v in vertices:
            out.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for e in sorted(edges):
            out.write(f"e {e[0]} {e[1]}\n")

if __name__ == "__main__":
    convert_obj_a_modelo("c:/Users/MC_SERVER/Downloads/10076_pisa_tower_v1_L1.123c0ccc34ea-97de-4741-a396-8717684fbc42/10076_pisa_tower_v1_L1.123c0ccc34ea-97de-4741-a396-8717684fbc42/10076_pisa_tower_v1_max2009_it0.obj", "torre_pisa.txt")
