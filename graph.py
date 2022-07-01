from tkinter import *
from tkinter import messagebox
import time

class BST:
    def __init__(self, root):
        self.window = root
        self.make_canvas = Canvas(self.window,width=1000,height=800,relief=RAISED)
        self.make_canvas.place(x=0,y=0)

        self.make_null = None
        self.insert_node = None
        self.take_entry = None
        self.make_node = None
        self.take_input = None
        self.add_btn = None
        self.make_label = None
        self.make_delete = None
        self.status_note = None

        
        self.animationTimeSide = 1
        self.animationTimeDown = 0.01
        self.notation_index = 0
        self.vertical_counter = 0
        self.take_arrow = 0
        self.right_activate = 1
        self.left_activate = 0
        self.position_controller = 0
        self.take_index = 0
        self.display_box_counter = -1

        self.label_position_x = 415
        self.label_position_y = 35+50

        self.gap_controller = 100

        self.node_number_value_store = []
        self.value_show = []
        self.temp_queue = []

        self.heading_root_and_null_make()
        self.make_instructional_buttons()
        self.make_container_in_result_canvas()
        self.make_horizontal_widget()

    def heading_root_and_null_make(self):
        self.make_null = Label(self.make_canvas)

    def make_instructional_buttons(self):
        self.take_entry = Entry(self.window, bd=3, bg="white")
        self.take_entry.place(x=20, y=80)
        self.take_entry.focus()
        self.add_btn = Button(self.window, width=10, bd=3)
        self.delete_btn = Button(self.window, width=10, bd=3)
        self.add_btn.place(x=20, y=120)
        self.delete_btn.place(x=20, y= 150)

        self.add_btn['text'] = "Add"
        self.delete_btn['text'] = 'Delete'
        self.window.unbind('<space>')
        self.add_btn['command'] =  lambda: self.filtration_of_input_value(False, 1)
        self.delete_btn['command'] = lambda: self.filtration_of_input_value(False, 2)
        self.window.bind('<Return>', lambda e: self.filtration_of_input_value(e, 1))
    
    def animationTime(self, value):
        if int(value) == 1:
            self.animationTimeSide = 1
            self.animationTimeDown = 0.01
        else:
            self.animationTimeSide = int(value) // 10
            self.animationTimeDown = int(value) // 100
        print(value)
    
    def make_horizontal_widget(self):
        self.scale_widget = Scale(self.window, from_=1, to=2, orient=HORIZONTAL, command=self.animationTime)
        self.scale_widget.place(x=20, y=180)

    def filtration_of_input_value(self, e, indicator):
        try:
            if int(self.take_entry.get()):
                    if indicator == 1:
                        if  len(self.node_number_value_store) == 0:
                            self.make_null.place_forget()
                        self.make_default_node_with_set_position()
                    else:
                        if self.node_number_value_store:
                           self.delete()
                        else:
                           messagebox.showerror("Empty BST", "Nothing to delete is BST")
        except:
            messagebox.showerror("Input Error", "Input value must be integer")

    def make_default_node_with_set_position(self):
        try:
            self.status_note.config(text="Insertion Process")
            self.status_note.place(x=20, y=20)

            self.make_node = self.make_canvas.create_oval(400, 70+50, 450, 20+50, width=2, fill="red")
            self.make_label= Label(self.window, text=self.take_entry.get(), fg="white", bg="red")
            self.make_label.place(x=self.label_position_x, y=self.label_position_y)
            if len(self.node_number_value_store) == 0:
                self.push_first_node()
            else:
                self.notation_index = 0
                self.position_controller = 70+80-5
                self.take_index = 0
                temp_take_val = self.take_entry.get()
                self.right_activate = 1
                self.gap_controller = 210
                self.left_activate = 0
                self.vertical_counter=0
                while True:
                    if self.right_activate == 1:
                        if self.position_controller <0:
                            self.position_controller = 25
                            self.left_movement_in_level()
                            self.position_controller = -1
                        else:
                            self.right_movement_in_level()
                    else:
                        self.left_movement_in_level()

                    if self.position_controller == -1 or self.position_controller == 70+self.gap_controller-5 or self.position_controller == 80+70+80+self.gap_controller-5:
                        break

                    if int(temp_take_val) < int(self.node_number_value_store[self.take_index][2]):
                        self.decision_making_about_left_side_direction()
                    elif int(temp_take_val) > int(self.node_number_value_store[self.take_index][2]):
                        self.decision_making_about_right_side_direction()
                    else:
                        messagebox.showerror("Duplicate Value Error","Duplicate Value by default not allowed in BST")
                        self.vertical_counter = 4
                        break

                    self.vertical_down_movement()

                    self.vertical_counter+=1
                    if self.vertical_counter == 3:
                        self.gap_controller -= 150
                    else:
                        self.gap_controller -= 85

                    if self.right_activate == 1:
                        self.right_moving_final_direction_giving()
                    elif self.left_activate == 1:
                        self.left_moving_final_direction_giving()

            if self.vertical_counter<=3:
                self.make_arrow()
            else:
                self.make_canvas.delete(self.make_node)
                self.make_label.place_forget()
                self.reset_and_store()
        except:
            print("Some force stop error")


    def delete(self):
        val = self.take_entry.get()
        p_node = None

        if len(self.node_number_value_store) == 0:
            messagebox.showwarning("Empty BST", "BST is empty..nothing to delete")
        else:
            node = self.node_number_value_store[0]
            while True:
                if node is None:
                    messagebox.showwarning("Not found","Sorry, targeting value not found")
                    break
                if int(node[2]) == int(val):
                    break
                if int(val)>int(node[2]):
                    p_node=node
                    node=node[6]
                else:
                    p_node = node
                    node=node[5]

            if node is not None:
                if node[5] is None and node[6] is None:
                    self.no_child_node_exist(node,p_node)

                elif node[5] is None and node[6] is not None:
                    self.left_none_right_exist(node)

                elif node[5] is not None and node[6] is None:
                    self.right_none_left_exist(node)

                elif node[5] is not None and node[6] is not None:
                    self.left_none_right_exist(node)

                if len(self.node_number_value_store) == 0:
                    self.notation_index = 0
                    self.make_null.place(x=565, y=90 + 50)

    def no_child_node_exist(self,node,p_node):
        if p_node is None:
            pass
        else:
            if p_node[5] is node:
                p_node[5] = None

            else:
                p_node[6] = None

        self.make_canvas.itemconfig(node[0], fill="blue", outline="black")
        node[1].config(bg="blue", fg="red")
        self.status_note.config(text="Blue colored node will deleted")
        self.status_note.place(x=20, y=20)
        self.window.update()
        time.sleep(1)
        self.make_canvas.delete(node[0])
        self.make_canvas.delete(node[4])
        node[1].place_forget()
        self.node_number_value_store.pop(self.node_number_value_store.index(node))
        print(self.node_number_value_store)
        self.status_note.config(text="Work done")
        self.status_note.place(x=20, y=20)

    def left_none_right_exist(self,node):
        p_temp = None
        temp = node[6]
        left_side_existence_checking_of_one_side_down_label_node=0
        while temp[5]:
            left_side_existence_checking_of_one_side_down_label_node=1
            p_temp=temp
            temp=temp[5]

        self.color_indicator_to_delete(node=node,temp=temp)

        if left_side_existence_checking_of_one_side_down_label_node == 1:
            node[2] = temp[2]
            node[1].config(text=temp[2])
            if temp[6]:
                temp[2] = temp[6][2]
                temp[1].config(text=temp[6][2])
                p_temp=temp
                temp=temp[6]
                p_temp[6]=None
            else:
                p_temp[5] = None
        else:
            temp1 = None
            p_temp=node
            while True:
                p_temp[2]=temp[2]
                p_temp[1].config(text=temp[2])
                if  temp[6]:
                    p_temp=temp
                    temp=temp[6]
                    if  temp[5]:
                        temp1 = temp[5]
                        temp[5] = None
                else:
                    break

            p_temp[6] = None

            if temp1:
                take_temp1_val = temp1[2]
                self.make_canvas.delete(temp1[0])
                self.make_canvas.delete(temp1[4])
                temp1[1].place_forget()
                self.node_number_value_store.pop(self.node_number_value_store.index(temp1))

                p_node_coord = self.make_canvas.coords(node[6][0])
                c_right_node_coord = self.make_canvas.coords(node[6][6][0])

                node_coord = self.make_node_to_the_left_manually(p_node_coord, c_right_node_coord)

                make_circle = self.make_canvas.create_oval(node_coord, width=3, fill="green", outline="black")

                arrow_coord = self.make_left_arrow_for_node_left_manually(node_coord, p_node_coord)

                take_arrow = self.make_canvas.create_line(arrow_coord, width=3, fill="brown")

                label_make = Label(self.window, text=take_temp1_val, fg="yellow", bg="green",
                                   font=("Arial", 12, "bold"))
                label_make.place(x=node_coord[0] + 14, y=node_coord[1] + 14)

                notation_index = ((node[6][3] + 1) * 2) - 1

                temp_take = self.store_all_data_about_a_node(make_circle, label_make, take_temp1_val, notation_index, take_arrow)

                node[6][5] = temp_take

        self.make_canvas.delete(temp[0])
        self.make_canvas.delete(temp[4])
        temp[1].place_forget()
        self.node_number_value_store.pop(self.node_number_value_store.index(temp))

        print(self.node_number_value_store)

    def right_none_left_exist(self, node):
        p_temp = None
        temp = node[5]
        right_side_existence_checking_of_one_side_down_label_node = 0
        while temp[6]:
            right_side_existence_checking_of_one_side_down_label_node = 1
            p_temp = temp
            temp = temp[6]

        self.color_indicator_to_delete(node=node, temp=temp)

        if  right_side_existence_checking_of_one_side_down_label_node == 1:
            node[2] = temp[2]
            node[1].config(text=temp[2])
            if temp[5]:
                temp[2] = temp[5][2]
                temp[1].config(text=temp[5][2])
                p_temp=temp
                temp=temp[5]
                p_temp[5]=None
            else:
                p_temp[6] = None

        else:
            temp1 = None
            p_temp = node
            while True:
                p_temp[2] = temp[2]
                p_temp[1].config(text=temp[2])
                if  temp[5]:
                    p_temp = temp
                    temp = temp[5]
                    if temp[6]:
                        temp1 = temp[6]
                        temp[6] = None
                else:
                    break

            p_temp[5] = None

            if temp1:
                take_temp1_val = temp1[2]
                self.make_canvas.delete(temp1[0])
                self.make_canvas.delete(temp1[4])
                temp1[1].place_forget()
                self.node_number_value_store.pop(self.node_number_value_store.index(temp1))

                p_node_coord = self.make_canvas.coords(node[5][0])
                c_right_node_coord = self.make_canvas.coords(node[5][5][0])

                node_coord = self.make_node_to_the_right_manually(p_node_coord, c_right_node_coord)

                make_circle = self.make_canvas.create_oval(node_coord, width=3, fill="green", outline="black")

                arrow_coord = self.make_right_arrow_for_node_right_manually(node_coord, p_node_coord)

                take_arrow = self.make_canvas.create_line(arrow_coord, width=3, fill="brown")

                label_make = Label(self.window, text=take_temp1_val, fg="yellow", bg="green", font=("Arial", 12, "bold"))
                label_make.place(x=node_coord[0] + 14, y=node_coord[1] + 14)

                notation_index = ((node[5][3] + 1) * 2)

                temp_take = self.store_all_data_about_a_node(make_circle,label_make,take_temp1_val,notation_index,take_arrow)
                node[5][6]=temp_take

        self.make_canvas.delete(temp[0])
        self.make_canvas.delete(temp[4])
        temp[1].place_forget()
        self.node_number_value_store.pop(self.node_number_value_store.index(temp))

        print(self.node_number_value_store)

    def color_indicator_to_delete(self,node,temp):
        self.make_canvas.itemconfig(temp[0], fill="brown")
        temp[1].config(bg="brown", fg="yellow")
        self.make_canvas.itemconfig(node[0], fill="yellow")
        node[1].config(bg="yellow", fg="green")

        self.status_note.config(text="Yellow colored node will deleted and replaced by brown colored node")
        self.status_note.place(x=20, y=20)
        self.window.update()
        time.sleep(5)

        self.make_canvas.itemconfig(temp[0], fill="green", outline="black")
        temp[1].config(fg="yellow", bg="green")
        self.make_canvas.itemconfig(node[0], fill="green", outline="black")
        node[1].config(fg="yellow", bg="green")
        self.status_note.config(text="Work done")
        self.status_note.place(x=20, y=20)

    def make_node_to_the_left_manually(self, p_node_coord, c_right_node_coord):
        make_initial_x = p_node_coord[0] - (c_right_node_coord[0] - p_node_coord[0])
        make_initial_y = c_right_node_coord[1]
        make_final_x = p_node_coord[2] - (c_right_node_coord[2] - p_node_coord[2])
        make_final_y = c_right_node_coord[3]
        node_coord = (make_initial_x, make_initial_y, make_final_x, make_final_y)
        return node_coord

    def make_left_arrow_for_node_left_manually(self, node_coord, p_node_coord):
        current_x = (node_coord[0] + node_coord[2]) / 2 + 18
        current_y = (node_coord[1] + node_coord[3]) / 2 - 18
        parent_x = (p_node_coord[0] + p_node_coord[2]) / 2 - 25
        parent_y = (p_node_coord[1] + p_node_coord[3]) / 2
        arrow_coord = (current_x, current_y, parent_x, parent_y)
        return arrow_coord

    def make_node_to_the_right_manually(self, p_node_coord, c_right_node_coord):
        make_initial_x = p_node_coord[0] + (p_node_coord[0] - c_right_node_coord[0])
        make_initial_y = c_right_node_coord[1]
        make_final_x = p_node_coord[2] + (p_node_coord[2] - c_right_node_coord[2])
        make_final_y = c_right_node_coord[3]
        node_coord = (make_initial_x, make_initial_y, make_final_x, make_final_y)
        return node_coord

    def make_right_arrow_for_node_right_manually(self, node_coord, p_node_coord):
        current_x = (node_coord[0] + node_coord[2]) / 2 - 18
        current_y = (node_coord[1] + node_coord[3]) / 2 - 18
        parent_x = (p_node_coord[0] + p_node_coord[2]) / 2 + 25
        parent_y = (p_node_coord[1] + p_node_coord[3]) / 2
        arrow_coord = (current_x, current_y, parent_x, parent_y)
        return arrow_coord

    def make_arrow(self):
        if self.notation_index == 0:
           self.take_arrow = -1
        else:
           for take in self.node_number_value_store:
               if int((self.notation_index-1)/2) == take[3]:
                     take_current = self.make_canvas.coords(self.make_node)
                     take_parent = self.make_canvas.coords(take[0])
                     if self.right_activate == 1:
                         if  self.vertical_counter == 3:
                             current_x = (take_current[0] + take_current[2]) / 2 - 2
                             current_y = (take_current[1] + take_current[3]) / 2 - 25
                             parent_x = (take_parent[0] + take_parent[2]) / 2 + 12
                             parent_y = (take_parent[1] + take_parent[3]) / 2 + 24
                             arrow_coord = (current_x,current_y,parent_x,parent_y)
                         else:
                             arrow_coord = self.right_side_arrow_coordinate_maker(take_current,take_parent)
                     else:
                         if self.vertical_counter == 3:
                             current_x = (take_current[0] + take_current[2]) / 2
                             current_y = (take_current[1] + take_current[3]) / 2 -25
                             parent_x = (take_parent[0] + take_parent[2]) / 2 - 18
                             parent_y = (take_parent[1] + take_parent[3]) / 2 + 19
                             arrow_coord = (current_x, current_y, parent_x, parent_y)
                         else:
                             arrow_coord = self.left_side_arrow_coordinate_maker(take_current,take_parent)
                     self.take_arrow = self.make_canvas.create_line(arrow_coord, width=3, fill="blue")
                     break

        self.store_data()

    def store_data(self):
        node_data = self.store_all_data_about_a_node(self.make_node,  self.make_label, self.take_entry.get(), self.notation_index, self.take_arrow)
        if self.notation_index > 0:
            parent_node_index = int((self.notation_index-1)/2)
            for  temp1 in self.node_number_value_store:
                 if temp1[3] == parent_node_index:
                     if self.notation_index%2 == 0:
                         temp1[6] = node_data
                     else:
                         temp1[5] = node_data

        self.reset_and_store()

    def reset_and_store(self):
        self.label_position_x = 415
        self.label_position_y = 35+50
        print(self.node_number_value_store)

        self.status_note.config(text="Work done")
        self.status_note.place(x=20, y=20)

    def right_side_arrow_coordinate_maker(self, take_current, take_parent):
        current_x = (take_current[0] + take_current[2]) / 2 - 18
        current_y = (take_current[1] + take_current[3]) / 2 - 18
        parent_x = (take_parent[0] + take_parent[2]) / 2 + 25
        parent_y = (take_parent[1] + take_parent[3]) / 2
        arrow_coord = (current_x,current_y,parent_x,parent_y)
        return arrow_coord

    def left_side_arrow_coordinate_maker(self, take_current, take_parent):
        current_x = (take_current[0] + take_current[2]) / 2 + 18
        current_y = (take_current[1] + take_current[3]) / 2 - 18
        parent_x = (take_parent[0] + take_parent[2]) / 2 - 25
        parent_y = (take_parent[1] + take_parent[3]) / 2
        arrow_coord = (current_x,current_y,parent_x,parent_y)
        return arrow_coord

    def push_first_node(self):
        x_move_counter = 0
        while x_move_counter < 70 - 5:
            self.make_label.place_forget()
            self.label_position_x += 2
            self.make_label.place(x=self.label_position_x, y=self.label_position_y)
            self.make_canvas.move(self.make_node, 2, 0)
            x_move_counter += 2
            self.window.update()

    def right_movement_in_level(self):
        try:
            x_move_counter = 0
            while x_move_counter < self.position_controller:
                self.make_label.place_forget()
                self.label_position_x += 2
                self.make_label.place(x=self.label_position_x, y=self.label_position_y)
                self.make_canvas.move(self.make_node, 2, 0)
                x_move_counter += 2
                self.window.update()
        except:
            print("Some force stop error")

    def left_movement_in_level(self):
        try:
            x_move_counter = 0
            while x_move_counter < self.position_controller:
                self.make_label.place_forget()
                self.label_position_x -= 2
                self.make_label.place(x=self.label_position_x, y=self.label_position_y)
                self.make_canvas.move(self.make_node, -2, 0)
                x_move_counter += 2
                self.window.update()
        except:
            print("Some force stop error")

    def decision_making_about_left_side_direction(self):
        try:
            self.left_activate = 1
            self.right_activate = 0
            self.window.update()
            time.sleep(self.animationTimeSide)
        except:
            print("Some force stop error")

    def decision_making_about_right_side_direction(self):
        try:
            self.right_activate = 1
            self.left_activate = 0
            self.window.update()
            time.sleep(self.animationTimeSide)
        except:
            print("Some force stop error")

    def vertical_down_movement(self):
        try:
            y_move_counter = 0
            while y_move_counter < 106:
                self.make_label.place_forget()
                self.label_position_y += 4
                self.make_label.place(x=self.label_position_x, y=self.label_position_y)
                self.make_canvas.move(self.make_node, 0, 4)
                y_move_counter += 4
                time.sleep(self.animationTimeDown)
                self.window.update()
        except:
            print("Some force stop error")

    def right_moving_final_direction_giving(self):
        try:
            for take in self.node_number_value_store:
                if int((self.notation_index + 1) * 2) == int(take[3]):
                    self.take_index = self.node_number_value_store.index(take)
                    self.position_controller = 70 + 80 + self.gap_controller - 5
                    break
            else:
                if self.vertical_counter == 3:
                    self.position_controller = -1
                else:
                    self.position_controller = 70 + self.gap_controller - 5
            self.notation_index = (self.notation_index + 1) * 2
        except:
            print("Some force stop error in final positioning")

    def left_moving_final_direction_giving(self):
        try:
            for take in self.node_number_value_store:
                if int((self.notation_index + 1) * 2) - 1 == int(take[3]):
                    self.take_index = self.node_number_value_store.index(take)
                    self.position_controller = 80 + 70 + self.gap_controller - 5
                    break
            else:
                self.position_controller = 80 + 70 + 80 + self.gap_controller - 5
            self.notation_index = ((self.notation_index + 1) * 2) - 1
        except:
            print("Some force stop error in final positioning")

    def make_container_in_result_canvas(self):
        self.status_note = Label(self.make_canvas, text="BST Status",font=("Arial", 20))
        self.status_note.place(x=20,y=20)
        
    def store_all_data_about_a_node(self,make_circle,label_make,take_temp1_val,notation_index,take_arrow):
        temp_take = []
        temp_take.append(make_circle)
        temp_take.append(label_make)
        temp_take.append(take_temp1_val)
        temp_take.append(notation_index)
        temp_take.append(take_arrow)
        temp_take.append(None)
        temp_take.append(None)
        self.node_number_value_store.append(temp_take)
        return temp_take


if __name__ == '__main__':
    window = Tk()
    window.title("BST")
    window.geometry("1000x800")
    window.resizable(False, False)
    BST(window)
    window.mainloop()
