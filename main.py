import locale
import os
import warnings

import matplotlib.pyplot as plt
import pandas as pd

plt.style.use(['seaborn-whitegrid', 'ggplot', 'fast'])

warnings.filterwarnings('ignore')
locale.setlocale(locale.LC_ALL, 'pt_BR')


def main():
    for dirname, _, filenames in os.walk('d:/data/dataset/covid/'):
        for filename in filenames:
            df = pd.read_csv(os.path.join(dirname, filename), sep=',', encoding='utf-8')
            df.rename(columns=str.lower, inplace=True)
            df.rename(columns=str.strip, inplace=True)
            df.dropna()

            df['date_reported'] = df['date_reported'].str.replace(",", "").str.strip()
            df['date_reported'] = pd.to_datetime(df['date_reported'], format="%Y-%m-%d")
            df['new_cases'] = df['new_cases'].fillna(0)
            df['cumulative_cases'] = df['cumulative_cases'].fillna(0)
            df['new_deaths'] = df['new_deaths'].fillna(0)
            df['cumulative_deaths'] = df['cumulative_deaths'].fillna(0)
            df['month'] = pd.DatetimeIndex(df['date_reported']).month

            # Soma os casos por País.
            grouped = df[['country', 'cumulative_cases', 'cumulative_deaths']].groupby('country'). \
                sum(). \
                reset_index()
            # filtered = grouped.query('cumulative_deaths > 0')
            # filtered = grouped.nlargest(20, ['cumulative_cases', 'cumulative_deaths'])
            # filtered = filtered.sort_values(by=['cumulative_cases', 'cumulative_deaths'], ascending=False)
            filtered = grouped.nlargest(10, ['cumulative_deaths'])
            filtered = filtered.sort_values(by=['cumulative_deaths'], ascending=False)
            filtered.columns = ['country', 'cumulative_cases', 'cumulative_deaths']
            filtered.loc[filtered['country'] == 'United States of America', 'country'] = 'USA'
            filtered.loc[filtered['country'] == 'Russian Federation', 'country'] = 'Russia'
            filtered.loc[filtered['country'] == 'The United Kingdom', 'country'] = 'England'
            filtered.loc[filtered['country'] == 'Iran (Islamic Republic of)', 'country'] = 'Iran'
            filtered.loc[filtered['country'] == 'Bolivia (Plurinational State of)', 'country'] = 'Bolivia'
            filtered.loc[filtered['country'] == 'Venezuela (Bolivarian Republic of)', 'country'] = 'Venezuela'
            filtered.loc[filtered['country'] == 'Republic of Korea', 'country'] = 'Korea'
            filtered.loc[filtered[
                             'country'] == 'occupied Palestinian territory, including east Jerusalem', 'country'] = 'Palestine'
            filtered.loc[filtered['country'] == 'Democratic Republic of the Congo', 'country'] = 'Congo'
            filtered.loc[filtered[
                             'country'] == 'Northern Mariana Islands (Commonwealth of the)', 'country'] = 'Northern Mariana Islands'
            labels = list(filtered['country'])
            # values_cc = list(filtered['cumulative_cases'].values)
            values_cd = list(filtered['cumulative_deaths'].values)
            print(labels)

            fig, ax = plt.subplots()
            # bar1 = ax.bar(labels, values_cc, label='Total de Casos')
            bar1 = ax.bar(labels, values_cd, label='Total de Mortes')

            def set_ticks(obj):
                """
                Anexa um texto acima de cada barra mostrando seu valor.
                """
                for item in obj:
                    height = item.get_height()
                    x = item.get_x() + item.get_width() / 2.
                    y = 1.05 * height
                    s = '{:n}'.format(int(height))
                    ax.text(x=x, y=y, s=s, ha='center', va='bottom')

            set_ticks(bar1)
            # set_ticks(bar2)

            # ax.set_ylabel('Escala')
            ax.set_title('Mortes por Covid-19')
            ax.legend()

            plt.show()


if __name__ == '__main__':
    main()
