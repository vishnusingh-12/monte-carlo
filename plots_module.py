import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_msd(mc_steps, paths, linestyle='dashed', ):
    x_val = [i for i in range(1, mc_steps // 2 + 1, 100)]
    marker_indices = [0] + [j for j in range(99, mc_steps // 200, 100)]
    color = ['tab:blue', 'tab:red', 'tab:green', 'tab:purple', 'tab:orange', 'tab:brown']
    markers = ['o', 's', '^', '*', 'p', 'd']
    if len(paths) > 6:
        print("Maximum 6 plots on a figure are allowed")
    else:
        for i in range(len(paths)):
            plt.plot(x_val, np.load(paths[i]), linestyle=linestyle, color=color[i])
            plt.scatter([x_val[k] for k in marker_indices],
                        [np.load(paths[i])[b] for b in marker_indices],
                        marker=markers[i], color=color[i], label=f'r={paths[i][-7:-4]}', s=50)
    plt.title(f"MSD vs MC steps for {100-int(paths[0][27:29])}% coverage")
    plt.xlabel('Steps')
    plt.ylabel('MSD')
    plt.legend()
    plt.show()


def plot_diffusivity():
    linestyle = 'dashed'
    color = ['tab:blue', 'tab:red', 'tab:green', 'tab:purple', 'tab:orange']
    markers = ['s', '^', '*', 'p', 'd']
    x_val = [i for i in range(10, 100, 10)]
    plt.plot(x_val[::-1], np.load('diffusivity_data/diffusivity.npy'), marker='o', color='black', linestyle=linestyle,
             label='Random Walk')
    ratio = 0.5
    for i in range(4):
        plt.plot(x_val[::-1], np.load(f'diffusivity_data/diffusivity_metro_{ratio}.npy'), marker=markers[i],
                 color=color[i], linestyle=linestyle, label=f'r = {ratio}')
        ratio += 0.5
    plt.legend()
    plt.show()


def plot_energy_heatmap(lattice):
    # Plot the final heatmap using sns.heatmap with custom color bar values
    ax = sns.heatmap(lattice.get_energy_lattice(), cmap='Reds', cbar=True, xticklabels=5, yticklabels=5)

    # Rotate the color bar label using Matplotlib
    cbar = ax.collections[0].colorbar
    cbar.ax.set_ylabel('x ε', rotation=0, labelpad=15)

    plt.title(f'Energy Penalties at {100-round(lattice.vacancy * 100)}% coverage')
    plt.show()
