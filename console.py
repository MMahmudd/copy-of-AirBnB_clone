#!/usr/bin/python3
""" Console_module_for the HBNB command_interpreter """

import cmd
from datetime import datetime
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import shlex  # for_splitting the_line

classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class HBNBCommand(cmd.Cmd):
    """ HBNH_console """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """ Exits the_console """
        return True

    def emptyline(self):
        """ Do nothing_on empty_line """
        pass

    def do_quit(self, arg):
        """ Quit command_to exit_the_program """
        return True

    def _key_value_parser(self, args):
        """ Parses_a list_of strings_into a_dictionary """
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """ Creates_a new_instance of a_class """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """ Prints_the string representation_of
        an instance_based on_the class_and id """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """ Deletes_an instance_based on the class_and id """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """ Prints_the string_representations of
        all_instances or of_instances of a_specific_class """
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        """ Updates an instance_based on
        the_class, id, attribute, and_value """
        args = shlex.split(arg)
        integers = ["number_rooms", "number_bathrooms", "max_guest", "price_by_night"]
        floats = ["latitude", "longitude"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] == "Place":
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except:
                                        args[3] = 0.0
                            setattr(models.storage.all()[k], args[2], args[3])
                            models.storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
