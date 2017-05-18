#include <gtk/gtk.h>

int joueurId=0,nbCoup=0;
const gchar *joueurs[2]={"joueur1","joueur2"};

///////////////////////////////////////////////////////////////////////////////
// Affichage d'un message dans la barre d'état
// Si withReset est TRUE, on efface tous les messages précédents
///////////////////////////////////////////////////////////////////////////////
void displayStatus(GtkBuilder *builder,gchar *msg,gboolean withReset) {
  if (builder==NULL) return;
  GtkStatusbar *status=(GtkStatusbar *)gtk_builder_get_object(builder,
                                                              "statusbar1");
  if (status!=NULL) {
    int id=gtk_statusbar_get_context_id(status,"info");
    if (withReset==TRUE) gtk_statusbar_remove_all(status,id);
    gtk_statusbar_push(status,id,msg);
  }
}
///////////////////////////////////////////////////////////////////////////////
// Affichage du prochain joueur dans la barre d'état
///////////////////////////////////////////////////////////////////////////////
void displayJoueur(GtkBuilder *builder) {
  if (builder==NULL) return;
  gchar *msg=NULL;
  if (nbCoup>=9) {
    msg=g_markup_printf_escaped("Partie terminée !");
  } else {
    msg=g_markup_printf_escaped("%s à vous de jouer...",joueurs[joueurId]);
  }
  if (msg!=NULL) {
    displayStatus(builder,msg,FALSE);
    g_free(msg);
  }
}
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void on_button_clicked(GtkWidget* src,gpointer data) {
  GtkBuilder *builder=GTK_BUILDER(data);
  if (builder!=NULL) {
    gtk_widget_set_sensitive(src,FALSE);
    GtkStyleContext *ctx=gtk_widget_get_style_context(src);
    if (ctx!=NULL) {
      gtk_style_context_add_class(ctx,joueurs[joueurId]);
    }
    nbCoup++;
    joueurId=(joueurId==0)?1:0; // Joueur suivant
    displayJoueur(builder);
  }
}
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void on_actionNewGame_activate(GtkAction* action,gpointer data) {
  printf("on_actionNewGame_activate...\n");
}
void on_actionAbout_activate(GtkAction* action,gpointer data) {
  printf("on_actionAbout_activate...\n");
}
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void on_actionQuit_activate(GtkAction* action,gpointer data) {
  GtkBuilder *builder=GTK_BUILDER(data);
  if (builder!=NULL) {
    GtkWindow *window=(GtkWindow *)gtk_builder_get_object(builder,"window1");
    if (window!=NULL) {
      GtkApplication *app=gtk_window_get_application(window);
      if (app!=NULL) {
        gtk_application_remove_window(app,window);
      }
    }
  }
}
///////////////////////////////////////////////////////////////////////////////
// Chargement de la mise en forme CSS
///////////////////////////////////////////////////////////////////////////////
void loadCSS() {
  GtkCssProvider *provider=gtk_css_provider_new();
  GdkDisplay *display=gdk_display_get_default();
  GdkScreen *screen=gdk_display_get_default_screen(display);
  gtk_style_context_add_provider_for_screen(screen,
                                            GTK_STYLE_PROVIDER(provider),
                                            GTK_STYLE_PROVIDER_PRIORITY_USER);
  GError *error=NULL;
  gtk_css_provider_load_from_path(provider,"style.css",&error);
  if (error!=NULL) {
    fprintf(stderr,"Unable to load CSS file: %s !\n",error->message);
    g_error_free(error);
  }
  g_object_unref(provider);
}
///////////////////////////////////////////////////////////////////////////////
// Création de la fenêtre et de son contenu avec GtkBuilder
///////////////////////////////////////////////////////////////////////////////
static void startApplication(GtkApplication* app,gpointer data) {
  loadCSS();
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
  GtkApplication *app=gtk_application_new("fr.iutbeziers.tictactoe-2",
                                          G_APPLICATION_FLAGS_NONE);
  g_signal_connect(app,"activate",G_CALLBACK(startApplication),NULL);
  int status=g_application_run(G_APPLICATION(app),argc,argv);
  g_object_unref(app);
  return status;
}
