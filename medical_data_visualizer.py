import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# 1 Add 'overweight' column
height_m = df['height'] / 100
bmi = df['weight'] / (height_m ** 2)
df['overweight'] = (bmi > 25).astype(int)

# 2 Normalize data: 0 = good, 1 = bad for 'cholesterol' and 'gluc'
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)


def draw_cat_plot():
    # 3 Create DataFrame for cat plot using pd.melt
    df_cat = pd.melt(df,
                     id_vars=['cardio'],
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # 4 Group and reformat the data to show counts
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # 5 Draw the catplot
    cat = sns.catplot(x='variable', y='total', hue='value', col='cardio', kind='bar', data=df_cat)

    # 6 Get figure for output
    fig = cat.fig
    return fig


def draw_heat_map():
    # Clean the data
    df_heat = df.copy()

    # Keep rows where ap_lo <= ap_hi
    df_heat = df_heat[df_heat['ap_lo'] <= df_heat['ap_hi']]

    # Remove height outliers
    height_low = df_heat['height'].quantile(0.025)
    height_high = df_heat['height'].quantile(0.975)
    df_heat = df_heat[(df_heat['height'] >= height_low) & (df_heat['height'] <= height_high)]

    # Remove weight outliers
    weight_low = df_heat['weight'].quantile(0.025)
    weight_high = df_heat['weight'].quantile(0.975)
    df_heat = df_heat[(df_heat['weight'] >= weight_low) & (df_heat['weight'] <= weight_high)]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 10))

    # Draw the heatmap
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', vmax=0.3, center=0, square=True, linewidths=.5, cbar_kws={'shrink': .5})

    return fig


if __name__ == '__main__':
    # Quick manual check: save the figures
    cat_fig = draw_cat_plot()
    cat_fig.savefig('catplot.png')

    heat_fig = draw_heat_map()
    heat_fig.savefig('heatmap.png')
