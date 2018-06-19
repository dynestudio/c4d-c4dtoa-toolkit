import c4d
from c4d import gui

# parameter ids (from arnold_procedural.h)
C4DAI_PROCEDURAL_NUM_PARAM_OVERRIDES = 500
C4DAI_PROCEDURAL_PARAM_OVERRIDE_SEP = 10000
C4DAI_PROCEDURAL_PARAM_OVERRIDE_SELECTION = 10001
C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE = 10002
C4DAI_PROCEDURAL_PARAM_OVERRIDE_SHADER = 10003
C4DAI_PROCEDURAL_PARAM_OVERRIDE_SHADER_INDEX = 10004
C4DAI_PROCEDURAL_PARAM_OVERRIDE_EXPRESSION = 10005
C4DAI_PROCEDURAL_PARAM_OVERRIDE_PARAM_NAME = 10006
C4DAI_PROCEDURAL_PARAM_OVERRIDE_COLOR_VALUE = 10007
C4DAI_PROCEDURAL_PARAM_OVERRIDE_FLOAT_VALUE = 10008
C4DAI_PROCEDURAL_PARAM_OVERRIDE_INT_VALUE = 10009

C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__EXPR = 0
C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__SHADER = 1
C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__COLOR = 2
C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__FLOAT = 3
C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__INT = 4

# Class to represent a parameter override.
class ParameterOverride:
    def __init__(self):
        self.selection = ""
        self.mode = C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__EXPR
        self.expression = ""
        self.shader = None
        self.shader_index = 0
        self.param = ""
        self.color_value = c4d.Vector(0.0)
        self.float_value = 0.0
        self.int_value = 0

    def __str__(self):
        value = ""
        
        value += "Selection: %s\n" % self.selection
        if self.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__EXPR:
            value += "Mode: Expression\n"
            value += "Expression: %s\n" % self.expression
        elif self.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__SHADER:
            value += "Mode: Shader\n"
            value += "Shader: %s\n" % (self.shader.GetName() if self.shader is not None else "<none>")
            value += "Index: %d\n" % self.shader_index
        elif self.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__COLOR:
            value += "Mode: Color\n"
            value += "Param: %s\n" % self.param
            value += "Color: %f %f %f\n" % (self.color_value.x, self.color_value.y, self.color_value.z)
        elif self.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__FLOAT:
            value += "Mode: Float\n"
            value += "Param: %s\n" % self.param
            value += "Float: %f\n" % self.float_value
        elif self.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__INT:
            value += "Mode: Int\n"
            value += "Param: %s\n" % self.param
            value += "Int: %d\n" % self.int_value
            
        return value
                        
    def __eq__(self, other):
        if self.selection != other.selection or self.mode != other.mode:
            return False
        
        if self.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__EXPR:
            if self.expression != other.expression:
                return False
        elif self.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__SHADER:
            if self.shader != other.shader or self.shader_index != other.shader_index:
                return False
        elif self.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__COLOR:
            if self.param != other.param or self.color_value != other.color_value:
                return False
        elif self.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__FLOAT:
            if self.param != other.param or self.float_value != other.float_value:
                return False
        elif self.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__INT:
            if self.param != other.param or self.int_value != other.int_value:
                return False
                    
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)    

# Reads the current parameter overrides of the given Arnold Procedural object.
def ReadParameterOverrides(proc):
    overrides = []
    
    numParamOverrides = proc[C4DAI_PROCEDURAL_NUM_PARAM_OVERRIDES]
    for i in range(numParamOverrides):
        offset = i * 100

        override = ParameterOverride()
        override.selection = proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_SELECTION + offset]
        override.mode = proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE + offset]
        if override.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__EXPR:
            override.expression = proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_EXPRESSION + offset]
        elif override.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__SHADER:
            override.shader = proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_SHADER + offset]
            override.shader_index = proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_SHADER_INDEX + offset]
        elif override.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__COLOR:
            override.param = proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_PARAM_NAME + offset]
            override.color_value = proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_COLOR_VALUE + offset]
        elif override.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__FLOAT:
            override.param = proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_PARAM_NAME + offset]
            override.float_value = proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_FLOAT_VALUE + offset]
        elif override.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__INT:
            override.param = proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_PARAM_NAME + offset]
            override.int_value = proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_INT_VALUE + offset]
            
        overrides.append(override)
                
    return overrides
            
# Print out the current parameter overrides of the given Arnold Procedural object.
def ListParameterOverrides(proc):
    print "====================================================="
    print "Parameter overrides of %s" % proc.GetName()
    print "====================================================="
    overrides = ReadParameterOverrides(proc)
    print "Number of overrides: %d" % len(overrides)
    for i, override in enumerate(overrides):
        print " "
        print "%d. override" % (i+1) 
        print override

# Returns true when the given parameter override is already defined on the given Arnold Procedural object.
def IsParameterOverrideExists(proc, override):
    proc_overrides = ReadParameterOverrides(proc)
    for proc_override in proc_overrides:
        if proc_override == override:
            return True
    
    return False

# Adds a new parameter override to the given Arnold Procedural object.
def AddParameterOverride(proc, override):
    print "----------------"
    print "Add parameter override:"
    print override
    print " "
    
    # first check if the override already exists
    if IsParameterOverrideExists(proc, override):
        print "[WARNING] Override already exists"
        return

    # add a new override
    numParamOverrides = proc[C4DAI_PROCEDURAL_NUM_PARAM_OVERRIDES]
    proc[C4DAI_PROCEDURAL_NUM_PARAM_OVERRIDES] = numParamOverrides + 1
    offset = numParamOverrides * 100
      
    proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_SELECTION + offset] = override.selection
    proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE + offset] = override.mode
    if override.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__EXPR:
        proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_EXPRESSION + offset] = override.expression
    elif override.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__SHADER:
        proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_SHADER + offset] = override.shader
        proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_SHADER_INDEX + offset] = override.shader_index
    elif override.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__COLOR:
        proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_PARAM_NAME + offset] = override.param
        proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_COLOR_VALUE + offset] = override.color_value
    elif override.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__FLOAT:
        proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_PARAM_NAME + offset] = override.param
        proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_FLOAT_VALUE + offset] = override.float_value
    elif override.mode == C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__INT:
        proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_PARAM_NAME + offset] = override.param
        proc[C4DAI_PROCEDURAL_PARAM_OVERRIDE_INT_VALUE + offset] = override.int_value
        
    print "Override added successfully"
    
# Adds a new expression override to the given Arnold Procedural object.
def AddExpressionOverride(proc, selection, expression):
    override = ParameterOverride()
    override.selection = selection
    override.mode = C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__EXPR
    override.expression = expression

    AddParameterOverride(proc, override)

# Adds a new shader override to the given Arnold Procedural object.
def AddShaderOverride(proc, selection, mat, index):
    override = ParameterOverride()
    override.selection = selection
    override.mode = C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__SHADER
    override.shader = mat
    override.shader_index = index

    AddParameterOverride(proc, override)
        
# Adds a new color override to the given Arnold Procedural object.
def AddColorOverride(proc, selection, param, value):
    override = ParameterOverride()
    override.selection = selection
    override.mode = C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__COLOR
    override.param = param
    override.color_value = value

    AddParameterOverride(proc, override)
    
# Adds a new float override to the given Arnold Procedural object.
def AddFloatOverride(proc, selection, param, value):
    override = ParameterOverride()
    override.selection = selection
    override.mode = C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__FLOAT
    override.param = param
    override.float_value = value

    AddParameterOverride(proc, override)

# Adds a new integer override to the given Arnold Procedural object.
def AddIntOverride(proc, selection, param, value):
    override = ParameterOverride()
    override.selection = selection
    override.mode = C4DAI_PROCEDURAL_PARAM_OVERRIDE_MODE__INT
    override.param = param
    override.int_value = value

    AddParameterOverride(proc, override)


def main():
    # find the Arnold Procedural object
    proc = doc.SearchObject("Arnold Procedural")

    # list the current parameter overrides
    ListParameterOverrides(proc)
    
    # add new overrides
    AddExpressionOverride(proc, "/MyObject1", "my_param = 0.4")
    AddShaderOverride(proc, "/MyObject2", doc.SearchMaterial("Gold"), 1)
    AddColorOverride(proc, "/MyObject3", "my_color_param", c4d.Vector(0.1, 0.2, 0.3))
    AddFloatOverride(proc, "/MyObject4", "my_float_param", 1.35)
    AddIntOverride(proc, "/MyObject5", "my_int_param", 24)
    
    # update the scene
    c4d.EventAdd()

if __name__=='__main__':
    main()
