# dash-ma-plot

An interactive MA plot of RNA-seq data using python dash.

<img alt="Screenshot demo" src="./screenshots/MA-dash-10fps-50pc.gif" width=448 height=195>


## installation

Use the conda environment specified by `dash-env.yaml` which creates the environment "dash-ma-plot."

```
conda env create --file dash-env.yaml
```

This creates a conda environment with the necessary `dash` modules installed. Use the `--name` argument to
change the environment name, if desired.

## running

```
goober@gooberworld % conda activate dash-ma-plot
(dash) goober@gooberworld % python MA-plot-app.py
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'MA-plot-app'
 * Debug mode: on
```

Now open the IP address listed above in your browser. If you wish to stop the app, you can press CTRL-C in the terminal window where you started it.
