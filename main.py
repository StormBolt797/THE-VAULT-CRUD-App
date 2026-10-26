from website import create_app# imports createapp from int

app = create_app()# calls the create app function and assigns the returned app to this app

if __name__ == '__main__':
    app.run(debug=True)# runs app after making sure no syntax errors are there