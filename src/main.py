from controllers.predictor_controller import PredictorController


def main():
    app = PredictorController()
    window = app.create_main_window()
    window.mainloop()


if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n> Processo finalizado!")
    finally:
        print("\n> Processo finalizado!")
    quit()