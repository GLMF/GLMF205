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
// Désactive tous les boutons de la liste
///////////////////////////////////////////////////////////////////////////////
void disableAllButtons(GList *liste) {
  GList *child;
  for (child=liste;child!=NULL;child=g_list_next(child)) {
    gtk_widget_set_sensitive(child->data,FALSE);
  }
}
///////////////////////////////////////////////////////////////////////////////
// Ajoute la classe de victoire à un élément de la liste à partir de son index
///////////////////////////////////////////////////////////////////////////////
void markWin(GList *liste,int index) {
  if (liste!=NULL) {
    GtkWidget *p=(GtkWidget *)g_list_nth_data(liste,index);
    if (p!=NULL) {
      GtkStyleContext *ctx=gtk_widget_get_style_context(p);
      if (ctx!=NULL) gtk_style_context_add_class(ctx,"win");
    }
  }
}
///////////////////////////////////////////////////////////////////////////////
// Recherche de 3 symboles alignés
// Renvoi TRUE si un joueur a gagné
///////////////////////////////////////////////////////////////////////////////
int verificationVictoire(GtkBuilder *builder) {
  gboolean res=FALSE;
  int i,j;
  int win[8][3]={{0,1,2},{3,4,5},{6,7,8},// Horizontal
                 {0,3,6},{1,4,7},{2,5,8},// Vertical
                 {0,4,8},{2,4,6}};       // Diagonales
  if (builder!=NULL) {
    GtkWidget *grid=(GtkWidget *)gtk_builder_get_object(builder,"grid1");
    if (GTK_IS_CONTAINER(grid)) {
      GList *liste=gtk_container_get_children(GTK_CONTAINER(grid));
      GList *child;
      int n,data[9]; // Tableau temporaire de résultat
      for (child=liste,n=0;child!=NULL;child=g_list_next(child),n++) {
        GtkStyleContext *ctx=gtk_widget_get_style_context(child->data);
        if (ctx!=NULL) {
          if (gtk_style_context_has_class(ctx,joueurs[0])) {
            data[n]=1; // Symbole du joueur 1
          } else if (gtk_style_context_has_class(ctx,joueurs[1])) {
            data[n]=2; // Symbole du joueur 2
          } else { 
            data[n]=0; // Pas de symbole
          }
        }
      }
      // Teste les différents cas de victoire
      for (i=0;i<8;i++) {
        // Indice des 3 cases à tester
        int a=win[i][0],b=win[i][1],c=win[i][2];
        if (data[a]!=0&&data[a]==data[b]&&data[b]==data[c]) {
          markWin(liste,a);
          markWin(liste,b);
          markWin(liste,c);
          disableAllButtons(liste);
          gchar *msg=g_markup_printf_escaped("Le %s a gagné !",
                                             joueurs[joueurId]);
          displayStatus(builder,msg,FALSE);
          if (msg!=NULL) g_free(msg);
          res=TRUE;
          break;
        }
      }
      if (liste!=NULL) g_list_free(liste);
    }
  }
  return res;
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
    if (verificationVictoire(builder)!=TRUE) {
      nbCoup++;
      joueurId=(joueurId==0)?1:0; // Joueur suivant
      displayJoueur(builder);
    }
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
  GtkApplication *app=gtk_application_new("fr.iutbeziers.tictactoe-3",
                                          G_APPLICATION_FLAGS_NONE);
  g_signal_connect(app,"activate",G_CALLBACK(startApplication),NULL);
  int status=g_application_run(G_APPLICATION(app),argc,argv);
  g_object_unref(app);
  return status;
}
