from glob import glob


def open_file(File):
    with open(File, "r") as f:
        lines = f.read().split("\n")
    return lines

def gather_dependencies(lines):
    tmp = []
    for line in lines:
        if "import" in line:
            tmp.append(line)
    return tmp

dependencies = []
j_files = glob("*.java")
for j_file in j_files:
    lines = open_file(j_file)
    dependencies += gather_dependencies(lines)

deps = set(dependencies)
for dep in deps:
    print(dep)
