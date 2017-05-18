#include <gtk/gtk.h>

void on_button_clicked(GtkWidget* src,gpointer data) {
  printf("on_button_clicked...\n");
}
void on_actionNewGame_activate(GtkAction* action,gpointer data) {
  printf("on_actionNewGame_activate...\n");
}
void on_actionAbout_activate(GtkAction* action,gpointer data) {
  printf("on_actionAbout_activate...\n");
}
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void on_actionQuit_activate(GtkAction* action,gpointer data) {
  printf("on_actionQuit_activate...\n");
  GtkBuilder *builder=GTK_BUILDER(data);
  if (builder!=NULL) {
    GtkWindow *window=(GtkWindow *)gtk_builder_get_object(builder,"window1");
    if (window!=NULL) {
      GtkApplication *app=gtk_window_get_application(window);
      if (app!=NULL) {
        gtk_application_remove_window(app,window);
        printf("Bye bye !\n");
      }
    }
  }
}
///////////////////////////////////////////////////////////////////////////////
// Création de la fenêtre et de son contenu avec GtkBuilder
///////////////////////////////////////////////////////////////////////////////
static void startApplication(GtkApplication* app,gpointer data) {
  GtkBuilder *builder=gtk_builder_new_from_file("tictactoe.glade");
  if (builder!=NULL) {
    gtk_builder_connect_signals(builder,builder);
    GtkWidget *window=(GtkWidget *)gtk_builder_get_object(builder,"window1");
    if (window!=NULL) {
      gtk_application_add_window(app,GTK_WINDOW(window));
      gtk_widget_show_all(window);
    }
  }
}
///////////////////////////////////////////////////////////////////////////////
// Programme principal
///////////////////////////////////////////////////////////////////////////////
int main(int argc,char *argv[]) {
  GtkApplication *app=gtk_application_new("fr.iutbeziers.tictactoe-1",
                                          G_APPLICATION_FLAGS_NONE);
  g_signal_connect(app,"activate",G_CALLBACK(startApplication),NULL);
  int status=g_application_run(G_APPLICATION(app),argc,argv);
  g_object_unref(app);
  return status;
}
