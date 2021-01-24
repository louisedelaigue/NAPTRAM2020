import matplotlib.pyplot as plt

for file in file_list:
    data_dict[file].pH = data_dict[file].pH.astype(float)
    color='tab:blue'
    fig, ax1 = plt.subplots()
    ax1.scatter(data_dict[file].sec, data_dict[file].pH, s=2, color=color)
    # ax1.set_ylim([data_dict[file].pH.min, data_dict[file].pH.max,])
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('pH', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx() # command for second y axis for temp
    
    color='tab:red'
    ax2.scatter(data_dict[file].sec, data_dict[file].temp, s=2, color=color)
    ax2.set_ylabel('Temperature (°C)', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.suptitle()
    plt.tight_layout()
    plt.show()
