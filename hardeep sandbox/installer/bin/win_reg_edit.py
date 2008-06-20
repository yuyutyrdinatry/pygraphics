# Registry modification code obtained from:
# http://agiletesting.blogspot.com/2005/06/handling-path-windows-registry-value.html
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/416087
# http://socal-piggies.blogspot.com/2005/05/manipulating-windows-registry-values.html    
    
import os, sys
import _winreg

class WinRegistry:
    def __init__(self, reg=_winreg.HKEY_LOCAL_MACHINE,
                 key=r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"):
        self.reg = _winreg.ConnectRegistry(None, reg)
        self.key = key
    
    def create_subkey(self, subkey):
        key = self.key + "\\" + subkey
        _winreg.CreateKey(self.reg, key)
    
    def delete_subkey(self, subkey):
        key = self.key + "\\" + subkey
        _winreg.DeleteKey(self.reg, key)
    
    def set_value(self, value_name="", value="", subkey=None, value_type=_winreg.REG_EXPAND_SZ):
        key = self.key
        if subkey:
            key += "\\" + subkey
            
        k = _winreg.OpenKey(self.reg, key, 0, _winreg.KEY_WRITE)
        _winreg.SetValueEx(k, value_name, 0, value_type, value)
        _winreg.CloseKey(k)
    
    def get_value(self, value_name="", subkey=None):
        key = self.key
        if subkey:
            key += "\\" + subkey
            
        k = _winreg.OpenKey(self.reg, key)
        value = _winreg.QueryValueEx(k, value_name)[0]
        _winreg.CloseKey(k)
        
        return value
    
    def delete_value(self, value_name="", subkey=None):
        key = self.key
        if subkey:
            key += "\\" + subkey
            
        k = _winreg.OpenKey(self.reg, key, 0, _winreg.KEY_WRITE)
        _winreg.DeleteValue(k, value_name)
        _winreg.CloseKey(k)

if __name__ == '__main__':
    wr = WinRegistry()
    
    # Add ApplicationPath1 value_name to the Environment key
    value_name="ApplicationPath1"
    value="C:\\agent1\\agent.bat"
    wr.set_value(value_name, value, value_type=_winreg.REG_EXPAND_SZ)
    value = wr.get_value(value_name)
    print "Created value_name %s with value %s" % (value_name, value)
    # Now delete value_name
    print "Now deleting", value_name
    wr.delete_value(value_name)
    
    # Create subkey Environment\EnvTest1 and add ApplicationPath2 value_name to it
    subkey = "EnvTest1"
    value_name="ApplicationPath2"
    value="C:\\agent2\\agent.bat"
    wr.create_subkey(subkey)
    print "Created subkey", subkey
    wr.set_value(value_name, value, subkey)
    value = wr.get_value(value_name, subkey)
    print "Created value_name %s with value %s" % (value_name, value)
    # Now delete subkey
    print "Now deleting", subkey
    wr.delete_subkey(subkey)