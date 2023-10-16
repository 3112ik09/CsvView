from flask import Flask, render_template,request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64


def features(df):
    categorical_features = []
    numerical_features = []

    for column in df.columns:
        if df[column].dtype == 'object':
            if df[column].nunique() < 10:
                categorical_features.append(column)
        else:
            if df[column].nunique()!=df.shape[0]:
                numerical_features.append(column)

    return categorical_features, numerical_features


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('display.html', error='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('display.html', error='No selected file')
        if file:
            df = pd.read_csv(file)
            header = df.head().to_html()
            # df.drop("Id" , axis=1)
            categorical_features, numerical_features = features(df)

            pie_charts ={}
            for col in categorical_features:
                counts = df[col].value_counts()
                fig ,ax = plt.subplots()
                counts.plot.pie(autopct='%1.1f%%', ax=ax)
                ax.set_title(f'{col} (Categorical)')
                img = io.BytesIO()
                plt.savefig(img, format='png')
                img.seek(0)
                pie_charts[col] = base64.b64encode(img.getvalue()).decode()
                plt.close()

            histograms = {}
            for col in numerical_features:
                fig, ax = plt.subplots()
                df[col].plot.hist(bins=10, ax=ax)
                ax.set_title(f'{col} (Numerical)')
                img = io.BytesIO()
                plt.savefig(img, format='png')
                img.seek(0)
                histograms[col] = base64.b64encode(img.getvalue()).decode()
                plt.close()
            

            return render_template('display.html', header=header , pie_charts=pie_charts, histograms=histograms)

    return render_template('display.html')

if __name__ == '__main__':
    app.run(debug=True)