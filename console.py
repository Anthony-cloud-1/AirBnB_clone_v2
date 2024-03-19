#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dotted_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets represent optional fields in usage example.)
        """
        ln_cmd = ln_cls = ln_id = ln_args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            parline = line[:]  # parsed line

            # isolate <class name>
            ln_cls = parline[:parline.find('.')]

            # isolate and validate <command>
            ln_cmd = parline[parline.find('.') + 1:parline.find('(')]
            if ln_cmd not in HBNBCommand.dotted_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            parline = parline[parline.find('(') + 1:parline.find(')')]
            if parline:
                # partition args: (<id>, [<delim>], [<*args>])
                parline = parline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                ln_id = parline[0].replace('\"', '')
                # empty quotes register as empty ln_id when replaced

                # if arguments exist beyond ln_id
                parline = parline[2].strip()  # pline is now str
                if parline:
                    # check for *args or **kwargs
                    if parline[0] == '{' and parline[-1] == '}'\
                            and type(eval(parline)) is dict:
                        ln_args = parline
                    else:
                        ln_args = parline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([ln_cmd, ln_cls, ln_id, ln_args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        try:
            if not args:
                raise SyntaxError()
            arg_l = args.split(" ")
            kwa = {}
            for arg in arg_l[1:]:
                arg_split = arg.split("=")
                arg_split[1] = eval(arg_split[1])
                if type(arg_split[1]) is str:
                    arg_split[1] = arg_split[1].replace("_", " ").replace('"', '\\"')
                kwa[arg_split[0]] = arg_split[1]
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        new_inst = HBNBCommand.classes[arg_l[0]](**kwa)
        new_inst.save()
        print(new_inst.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        cls_name = new[0]
        cls_id = new[2]

        # guard against trailing args
        if cls_id and ' ' in cls_id:
            cls_id = cls_id.partition(' ')[0]

        if not cls_name:
            print("** class name missing **")
            return

        if cls_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not cls_id:
            print("** instance id missing **")
            return

        key = cls_name + "." + cls_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        cls_name = new[0]
        cls_id = new[2]
        if cls_id and ' ' in cls_id:
            cls_id = cls_id.partition(' ')[0]

        if not cls_name:
            print("** class name missing **")
            return

        if cls_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not cls_id:
            print("** instance id missing **")
            return

        key = cls_name + "." + cls_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_l = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for key, val in storage.all(HBNBCommand.classes[args]).items():
                print_l.append(str(val))
        else:
            for key, val in storage.all().items():
                print_l.append(str(val))
        print(print_l)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        counter = 0
        for key, val in storage._FileStorage__objects.items():
            if args == key.split('.')[0]:
                counter += 1
        print(counter)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        cls_name = cls_id = a_name = a_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            cls_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if cls_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            cls_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = cls_name + "." + cls_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for key, val in kwargs.items():
                args.append(key)
                args.append(val)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                scnd_quote = args.find('\"', 1)
                a_name = args[1:scnd_quote]
                args = args[scnd_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not a_name and args[0] != ' ':
                a_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                a_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not a_val and args[2]:
                a_val = args[2].partition(' ')[0]

            args = [a_name, a_val]

        # retrieve dictionary of current objects
        n_dict = storage.all()[key]

        # iterate through attr names and values
        for i, a_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                a_val = args[i + 1]  # following item is value
                if not a_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not a_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if a_name in HBNBCommand.types:
                    a_val = HBNBCommand.types[a_name](a_val)

                # update dictionary with name, value pair
                n_dict.__dict__.update({a_name: a_val})

        n_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
