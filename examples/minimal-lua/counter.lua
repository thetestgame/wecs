function(component) 
    
    -- Meta class
    Counter = {component = nil}

    -- Derived class method new
    function Counter:new(o, component)
       o = o or {}
       setmetatable(o, self)

       self.component = component or nil
       self.__index = self
       return o
    end

    -- Handles system update calls
    function Counter:update(entity)
        storage = self.component.script_storage
        counter = storage['CounterComponent']
        counter.value = counter.value + 1
    end

    return Counter:new(nil, component)
end