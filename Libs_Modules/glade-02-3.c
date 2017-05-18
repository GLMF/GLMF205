#include <gtk/gtk.h>

///////////////////////////////////////////////////////////////////////////////
// Création de la fenêtre et de son contenu avec GtkBuilder
///////////////////////////////////////////////////////////////////////////////
static void startApplication(GtkApplication* app,gpointer data) {
  GtkBuilder *builder=gtk_builder_new_from_file("cb02-3.glade");
  if (builder!=NULL) {
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
  GtkApplication *app=gtk_application_new("fr.iutbeziers.glade-02-3",
                                          G_APPLICATION_FLAGS_NONE);
  g_signal_connect(app,"activate",G_CALLBACK(startApplication),NULL);
  int status=g_application_run(G_APPLICATION(app),argc,argv);
  g_object_unref(app);
  return status;
}
