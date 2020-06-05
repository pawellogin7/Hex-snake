import numpy as np
import xml.etree.ElementTree as ET
import utils.snake_utilities as snake_utilities


class Replay:
    def __init__(self):
        self.replay_array = []
        self.temp_replay_array = []
        self.curr_frame_id = 0

    def add_board_frame(self, game_board):
        board_array = game_board.board_to_array()
        fruit_str = ''
        for i in range(len(board_array)):
            for j in range(len(board_array[0])):
                if game_board.board[i][j].type == 2:
                    fruit_str += '{}/{}/{}/'.format(j, i, game_board.board[i][j].fruit_type)
        # Informacje o graczu 1
        p1_str = ''
        p1_str += '{}/'.format(game_board.agents[0].direction)
        p1_str += '{}/'.format(game_board.agents[0].points)
        # Informacje o graczu 2
        p2_str = ''
        p2_str += '{}/'.format(game_board.agents[1].direction)
        p2_str += '{}/'.format(game_board.agents[1].points)
        self.temp_replay_array.append([fruit_str, p1_str, p2_str])

    def get_curr_frame(self):
        frame = self.replay_array[self.curr_frame_id]
        self.curr_frame_id += 1
        fruit_array = frame[0].split('/')
        p1_array = frame[1].split('/')
        p2_array = frame[2].split('/')
        frame = [fruit_array, p1_array, p2_array]
        return frame

    def load_replay(self, filepath):
        replay = []
        tree = ET.parse(filepath)
        replay_root = tree.getroot()
        for frame_xml in replay_root:
            frame_fruit = ''
            frame_p1 = ''
            frame_p2 = ''
            for elem in frame_xml:
                if elem.tag == 'fruit':
                    frame_fruit = elem.text
                elif elem.tag == 'player':
                    if elem.attrib['id'] == '1':
                        frame_p1 = elem.text
                    elif elem.attrib['id'] == '2':
                        frame_p2 = elem.text
            if frame_fruit == '' or frame_p1 == '' or frame_p2 == '':
                return False
            else:
                replay.append([frame_fruit, frame_p1, frame_p2])
        self.replay_array = replay
        return True

    def save_replay(self, filepath):
        replay_xml = ET.Element('replay')
        for frame in self.replay_array:
            frame_xml = ET.SubElement(replay_xml, 'frame')
            item_fruit = ET.SubElement(frame_xml, 'fruit')
            item_fruit.text = frame[0]
            item_p1 = ET.SubElement(frame_xml, 'player')
            item_p1.set('id', '1')
            item_p1.text = frame[1]
            item_p2 = ET.SubElement(frame_xml, 'player')
            item_p2.set('id', '2')
            item_p2.text = frame[2]
        xml_data = ET.tostring(replay_xml, 'ascii').decode('ascii')
        xml_data = xml_data.replace('><', '>\n<')
        xml_data = xml_data.replace('<frame', '\t<frame')
        xml_data = xml_data.replace('</frame', '\t</frame')
        xml_data = xml_data.replace('<fruit', '\t\t<fruit')
        xml_data = xml_data.replace('<player', '\t\t<player')
        xml_data = bytes(xml_data, 'ascii')
        file = open(filepath, 'wb')
        file.write(xml_data)
        file.close()
