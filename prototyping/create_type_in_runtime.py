
i = "12"
t=type(i)

new_value="123A"
new_var_same_type = t(new_value)
t2=t(new_var_same_type)
print(type(t2), t2)
