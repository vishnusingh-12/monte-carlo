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
                        marker=markers[i], color=color[i], label=f'$T^{"*"}$={round(1 / float(paths[i][-7:-4]), 2)}',
                        s=50)
    plt.title(f"MSD vs MC steps for {100 - int(paths[0][27:29])}% coverage")
    plt.xlabel('Steps')
    plt.ylabel('MSD')
    plt.legend()
    plt.show()


def plot_diffusivity():
    linestyle = 'dashed'
    color = ['tab:blue', 'tab:red', 'tab:green', 'tab:purple', 'tab:orange']
    markers = ['s', '^', '*', 'p', 'd']
    x_val = [10, 30, 50, 55, 60, 65, 70, 75, 80, 85, 90]
    # plt.plot(x_val[::-1], np.load('diffusivity_data/diffusivity.npy'), marker='o', color='black', linestyle=linestyle,
    #          label='Random Walk')
    ratio = [0.5, 0.57, 1.0, 1.5, 2.0]
    for i in range(5):
        plt.plot(x_val[::-1], np.load(f'diffusivity_data/40X40_T=1300_diffusivity_metro_{ratio[i]}(10-50 at 5,70,90).npy'),
                 marker=markers[i],
                 color=color[i], linestyle=linestyle, label=f'$T^{"*"}$ = {round(1 / ratio[i], 2)}')

        plt.legend()
        plt.title("Diffusivity vs Coverage, $T^{*}$= KT/\u03B5")
        plt.xlabel("Coverage")
        plt.ylabel("Diffusivity")
        plt.show()


def plot_energy_heatmap(lattice):
    # Plot the final heatmap using sns.heatmap with custom color bar values
    ax = sns.heatmap(lattice.energy_lattice, cmap='Reds', cbar=True, xticklabels=5, yticklabels=5)

    # Rotate the color bar label using Matplotlib
    cbar = ax.collections[0].colorbar
    cbar.ax.set_ylabel('x ε', rotation=0, labelpad=15)

    # Set color bar ticks to integers only
    cbar.set_ticks(cbar.get_ticks())

    ticks = cbar.get_ticks()
    cbar.set_ticks(np.round(ticks).astype(int))

    plt.title(f'Energy Penalties at {100 - round(lattice.vacancy * 100)}% coverage')
    plt.show()
