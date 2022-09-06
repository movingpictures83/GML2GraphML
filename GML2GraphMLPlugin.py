




class GML2GraphMLPlugin:
    def input(self, infile):
        self.in_gml = infile

    def run(self):
        pass

    def output(self, outfile):
        out_graphml = outfile

        graph_id = "GraphML Output"

        graphml_header = '<?xml version="1.0" encoding="UTF-8"?>\n' \
                 '<graphml xmlns="http://graphml.graphdrawing.org/xmlns"\n' \
                 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n' \
                 'xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns\n' \
                 'http://graphml.graphdrawing.org/xmlns/1.1/graphml.xsd">\n' \
                 '<key id="key_weight" for="edge" attr.name="weight" attr.type="double"/>\n' \
                 '<graph id="'+graph_id+'" edgedefault="directed">\n'

        # Write graph to dictionary:
        graph_dict = {}
        with open(self.in_gml, "r") as f_gml:
            node = False
            edge = False

            for line in f_gml.readlines():
                if line=="node [\n":
                    node=True
                elif line=="edge [\n":
                    edge=True
                elif line=="]\n":
                    node=False
                    edge=False

                if node:
                    if "id " in line:
                        id = line.split(" ")[1].strip("\n").strip('"')
                        graph_dict[id] = {}
                    elif "label " in line:
                        label = line.split(" ")[1].strip("\n").strip('"')
                        graph_dict[id]["label"] = label
                        graph_dict[id]["edges"] = []
                elif edge:
                    if "source " in line:
                        source = line.split(" ")[1].strip("\n").strip('"')
                    elif "target " in line:
                        target = line.split(" ")[1].strip("\n").strip('"')
                    elif "weight " in line:
                        weight = line.split(" ")[1].strip("\n").strip('"')
                        graph_dict[source]["edges"].append((graph_dict[target]["label"], weight))
        # Write dictionary to graphml file

        with open(out_graphml, "w") as f_graphml:
            # Write header:
            f_graphml.write(graphml_header)
            # Write nodes:
            for id in graph_dict.keys():
                line = '<node id="' + graph_dict[id]["label"] + '"/>\n'
                f_graphml.write(line)
            # Write edges:
            i=1
            for id in graph_dict.keys():
                for e, edge in enumerate(graph_dict[id]["edges"]):
                    line = '<edge id="{}" source="{}" target="{}">\n'.format("e"+str(i), graph_dict[id]["label"], graph_dict[id]["edges"][e][0])
                    line += '<data key="key_weight">{}</data>\n'.format(graph_dict[id]["edges"][e][1])
                    line += '</edge>\n'
                    f_graphml.write(line)
                    i+=1
