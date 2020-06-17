from django import template
register = template.Library()

def permission(parser, token):
    try:
        # get the arguments passed to the template tag; 
        # first argument is the tag name
        tag_name, username, permission, onkeyword, object = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly 4 arguments" % token.contents.split()[0])
    # look for the 'endpermission' terminator tag
    nodelist = parser.parse(('endpermission',))
    parser.delete_first_token()
    return PermissionNode(nodelist, username, permission, object)


class PermissionNode(template.Node):
    def __init__(self, nodelist, user, permission, object):
        self.nodelist = nodelist
        # evaluate the user instance as a variable and store
        self.user = template.Variable(user)
        # store the permission string
        self.permission = permission
        # evaluate the object instance as a variable and store
        self.object = template.Variable(object)

    def render(self, context):
        print(context)
        input()
        user_inst = self.user.resolve(context)
        print(user_inst)
        input()
        print(self.object)
        input()
        object_inst = self.object.resolve(context)
        print(object_inst)
        input()
        print(user_inst)
        input()        
        # create a new permissions object by calling a permissions 
        # factory method of the model class
        permissions_obj = object_inst.permissions(user_inst)
        print(permissions_obj)
        input()
        content = self.nodelist.render(context)
        print(context)
        input()
        print(content)
        input()
        if hasattr(permissions_obj, self.permission):
            # check to see if the permissions object has the permissions method
            # provided in the template tag
            perm_func = getattr(permissions_obj, self.permission)
            # execute that permissions method
            if perm_func():
                return content 
        return ""

register.tag('permission', permission)