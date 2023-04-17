
import numpy as np
import matplotlib.pyplot as plt
from functions import *
from matplotlib import container
from plots import savefig, legend, errorbar



class linear_fit():
    from matplotlib.offsetbox import AnchoredText

   # Style des Diagramms

    style = ['default']
    

    size = 16
    def _size(self):
        BIG = self.size 
        SMALL = self.size * 0.6
        MID = self.size * 0.75
        plt.rc('font', size=MID)          # controls default text sizes
        plt.rc('axes', titlesize=BIG)     # fontsize of the axes title
        plt.rc('axes', labelsize=MID)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL)    # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL)    # legend fontsize
        plt.rc('figure', titlesize=BIG)  # fontsize of the figure title

    x_mittel = 0
    m_val = 1
    n_val = 1
    x_val = 1
    y_val = 1
    n_err = 0
    m_err = 0
    Vmn = 0


    # Ausfürhlichkeit der Infos die beim Fit ausgegeben werden
    detail = False

    #-----------------------------------------------------------------
    #least squares zur Angabe der Güte des Plots
    def __chi2(self, x_vals, y_vals, m, n):
        self.chi = round(((y_vals - m*x_vals - n)**2/self.y_err**2).sum(), 2)
        return self.chi


    #---WICHTIG!!!!!!!!!!!!---------------------------------------------------
    # Definiere Fehler des Scatter Plots ------------------------------------------
    # BEACHTE: falls der Fehler eine float-zahl ist, muss diese erst im [] geschrieben werden und mit der Anzahl der
    # Messwerte multiplizert werden, um eine Liste mit entsprechender Länge zu erstellen
    def set_y_error(self,yerr,var=True):
        # y_err muss ein Array sein. Wenn es nicht schon eins ist sondern ein skalar, dann erstelle ein array
        #if type(yerr) == np.ndarray or type(yerr) == list:
        if isinstance(yerr, (np.ndarray, list)):
            self.y_err = yerr
        elif type(yerr) == np.float64 or type(yerr) == float or type(yerr) == int:
            self.y_err = np.array([yerr])

        self.y_var = var

        return self.y_err

    def set_x_error(self,xerr, use = True):
        # x_err muss ein Array sein. Wenn es nicht schon eins ist sondern ein skalar, dann erstelle ein array
        if type(xerr) == np.ndarray or type(xerr) == list:
            self.x_err = xerr
        elif type(xerr) == np.float64 or type(xerr) == float or type(xerr) == int:
            self.x_err = np.array([xerr])
            
        self.x_var = use
        return self.x_err


    #setze individuelles Runden für m und n
    m_round = ''
    n_round = ''

    # extra boolean, um die Ergebnissausgabe zu verhindern
    HIDE = False

    # Gebe die Ergebnisse Aus 
    def print_res(self, result,name , hide):
        if hide == False:
            print('----------------------------')
            if name != '':
                print(name)
            if self.detail == True:
                print('x:', result['x'])
                print('x^2:', result['xx'])
                print('y:', result['y'])
                print('sigma^2:' , result['Vy'])
            m_str = error_round(result['m'], result['merr'])
            n_str = error_round(result['n'], result['nerr'])
            print(f'm: {m_str[0]} +- {m_str[1]}')
            print(f'n: {n_str[0]} +- {n_str[1]}')
            print('\u03C7^2:', self.chi)     # soll minimum sein für guten Fit
            print('----------------------------')


    def function_label(self, error_mode = 'plus-minus'):     # gibt als label die lineare funktion mit fehlern wieder
        try:
            if error_mode == 'plus-minus':
                str_vals = [0]*4
                for i,j in enumerate([self.m_val,self.m_err,self.n_val,self.n_err]):
                    str_vals[i] = np.array([j])
                str_vals[0], str_vals[1] = error_round(str_vals[0], str_vals[1])
                str_vals[2], str_vals[3] = error_round(str_vals[2], str_vals[3])
                self.legend_label[0] = f'$f(x) =({str_vals[0]}\\pm{str_vals[1]})x + ({str_vals[2]}\\pm{str_vals[3]})$'
            elif error_mode == 'parenthesis':
                m_str = error_round(self.m_val, self.m_err, error_mode='parenthesis')
                n_str = error_round(self.n_val, self.n_err, error_mode='parenthesis')
                self.legend_label[0] = f'$f(x) = {m_str}x\\pm{n_str}$'
            elif error_mode == 'scientific':
                # m_str = error_round(self.m_val, self.m_err, error_mode='scientific')[0]
                # n_str = error_round(self.n_val, self.n_err, error_mode='scientific')[0]
                # self.legend_label[0] = f'$f(x) = {m_str}x\\pm{n_str}$'
                print('function_label: error_mode = scientific ist noch nicht verfuegbar')
            else:
                print('function_label: error_mode exisitiert nicht. überprüfe, ob keine Rechtschreibfehler vorhanden sind')
                
        except:
            print('error: konnte legend_label nicht setzen')
        # print(error_round(self.n_val, self.n_err, error_mode='scientific')[0])
        # print(self.n_val, self.n_err)
        return

    # Erstelle Eigene Profile mit individuellen Aussehen
    def profile(self,name):
        if name == 'Gabriel':
            self.legendsize = 9
            self.errbar = [8,5,1,1,'x']
            self.plotsize = (6,4.5)
            self.size = 18
            self.function_label()
            self.style = ['science']
            self.grid = True
            
        elif name == 'Christian':
            self.errbar = [7,5,1.5,1.5,'x']
            self.plotsize = (10,6)
            self.ANCH = 25
            self.size = 25
            self.legendsize = 15
            self.colors[1] = 'cornflowerblue'
            self.function_label()
            self.style = ['science']
            self.grid = True
        else:
            print('profile not found')


    #---WICHTIG!!!!!!!!!!!!--------------------------------------------------- 
    # hiermit werden alle Daten nach belieben varianzgewichtet ausgewertet
    def make_fit(self,x_vals,y_vals ,r = 20, hide='', name = 'generic name', kafe2 = False):

        if hide != '':                                # kontrolliert, welchen Wert HIDE hat
            self.HIDE = hide
        
        if self.m_round == '':                        #setze m,n nachkommastellen
            self.m_round = r   

        if self.n_round == '':                        #setze m,n nachkommastellen
            self.n_round = r 
    

        #-setze die globalen variablen auf die Werte der make_fit function
        self.x_val=x_vals      
        self.y_val=y_vals

        #-breche Funktion ab, wenn y-fehler nicht definiert wurde, da dieser wichtig zur weiteren Berechnung ist 
        # (für die varianzgewichtete Standardabweichung)
        if self.y_err[0]==0:
            print('Achtung: bitte y-Fehler setzen')
            return 0

        # berechne mittelwerte (Varianzgewichtet) 
        # err ist dummy array für den error, falls der error nur eine float ist und kein array 
        # Dies ist wichtig zur einfachen Berechnung
        if kafe2 == False:
            return self._myfit(x_vals,y_vals ,r = r , name = name)
        else :
            return self._kafefit(x_vals,y_vals, name = name)
            
       

    def _myfit(self,x_vals,y_vals ,r = 20, name = 'generic name'):
        if self.y_var == True:
            if self.HIDE == False:
                print('VARIANZGEWICHTET')
            if len(self.y_err) == 1:
                err = np.zeros(len(x_vals))
                err[:] = float(self.y_err[0])
            else:
                err = self.y_err
            err = np.asarray(err)
            y = mittel_varianzgewichtet(y_vals,err)
        else:
        # nicht varianzgewichtet sind die Mittelwerte einfache arithmetische Mittel
            if self.HIDE == False:
                print('NICHT VARIANZGEWICHTET')
            y = np.mean(y_vals)
            
        if self.x_var == True:
            if len(self.x_err) == 1:
                err = np.zeros(len(x_vals))
                err[:] = float(self.x_err[0])
            else:
                err = self.x_err
            err = np.asarray(err)
            x = mittel_varianzgewichtet(x_vals,err)
            xx = mittel_varianzgewichtet(x_vals**2,err)
        else:
            x = np.mean(x_vals)
            xx = np.mean(x_vals**2)

        # zur Berechnung der Varianzen Vxy und Vx benötigen wir die Mittelwerte als arrays
        x_arr = np.zeros(len(x_vals))
        x_arr[:] = x
        y_arr = np.zeros(len(y_vals))
        y_arr[:] = y 
        
        # Berechne Varianzen
        # Vxy = varianz_xy(x_vals,x_arr,y_vals,y_arr)
        Vxy = varianz_xy(x_vals,y_vals)
        # Vx = varianz_x(x_vals,x_arr)
        Vx = varianz_x(x_vals)

        # Berechne y-Varianz. Unterscheide, ob es einen einheitlichen y-Fehler gibt oder jeder Messwert einen individuellen hat
        if len(self.y_err) == 1:
            Vy = len(x_vals) / (1/np.asarray(([self.y_err]*len(x_vals)))**2).sum()
        else:
            # Varianzgewichtete Varianz, da mit standardvarianz es nicht funktioniert
            Vy = len(x_vals) / (1/self.y_err**2).sum()    
        Vm = Vy/(len(x_vals)*(xx-x**2))
        Vn = xx * Vm
        Vmn = - Vm * x
        #sigma = np.sqrt(Vy)

        # Berechne die Steigung m und den Achsenabschnitt n der Geraden
        m = round(Vxy/Vx,self.m_round)
        n = round(y-m*x,self.n_round)
        m = Vxy/Vx
        n = y-m*x
        
        # ein Algorithmus, der nachträglich den Achsenabschnitt verschiebt, falls die Werte nicht gut passen
        i = 0.0001
        k = 0.0001
        while (self.__chi2(x_vals, y_vals, m, n) > self.__chi2(x_vals, y_vals, m, n + i*y)):
            n = n+i*y
            i += 0.0001
        while (self.__chi2(x_vals, y_vals, m, n) > self.__chi2(x_vals, y_vals, m, n - k*y)):
            n = n-k*y
            k += 0.0001
            
        
        
        # Berechne Fehler der Steigung m und des Achsenabschnitts n der Geraden
        merr = roundup(np.sqrt(Vm),self.m_round)
        nerr = roundup(np.sqrt(Vn),self.n_round)
        merr = np.sqrt(Vm)
        nerr = np.sqrt(Vn)

        # Verwandle floats ohne Nachkommastellen in integer
        if self.m_round == 0:
            m, merr = int(m), int(merr)
        if self.n_round == 0:
            n, nerr = int(n), int(nerr)

        # globale Variablen erhalten Werde der make_fit function
        self.m_err = merr
        self.n_err = nerr
        self.x_mittel = x
        self.n_val = n
        self.m_val = m
        self.Vmn = Vmn

        # Berechne die Güte mit der least_squares Methode

        result = {
            'x' :x,
            'xx' :xx,
            'y' :y,
            'm' : m,
            'n' : n,
            'merr' : merr,
            'nerr' : nerr,
            'Vm' : round(Vm,r),
            'Vn' : round(Vn,r),
            'Vxy' : round(Vxy,r),
            'Vy' : round(Vy,2),
            'Vmn' : round(Vmn,r),
            'goodness' : round(self.chi, 2),
            'x_vals' : x_vals,
            'y_vals' : y_vals,
            'yerr' : self.y_err,
            'xerr' : self.x_err,
            'name' : name
        }

        self.print_res(result,name = name ,hide=self.HIDE)
        
        return result
    
    def _kafefit(self,x_vals,y_vals, name = 'generic name'):
        
        import kafe2
        
        self.__get_error()
        if self.x_var == True:
            kafe_result = kafe2.xy_fit(x_vals, y_vals, y_error = self.y_err, x_error = self.x_err)
        else:
            kafe_result = kafe2.xy_fit(x_vals, y_vals, y_error = self.y_err)
            
        m, merr = kafe_result['parameter_values']['a'], kafe_result['parameter_errors']['a']
        n, nerr = kafe_result['parameter_values']['b'], kafe_result['parameter_errors']['b']
        goodness = kafe_result['goodness_of_fit']
        Vmn = kafe_result['parameter_cov_mat'][0,1]
        
        result = {
            'm' : m,
            'n' : n,
            'merr' : merr,
            'nerr' : nerr,
            'Vmn' : Vmn,
            'x_vals' : x_vals,
            'y_vals' : y_vals,
            'yerr' : self.y_err,
            'xerr' : self.x_err,
            'goodness': goodness,
            'name' : name
        }
        
        self.m_err = merr
        self.n_err = nerr
        #self.x_mittel = x
        self.n_val = n
        self.m_val = m
        self.Vmn = Vmn
        
        if self.HIDE == False:
            
            m_str = error_round(m, merr)
            n_str = error_round(n, nerr)
            print('-------------------------------------')
            print(name)
            print(f'm: {m_str[0]} +- {m_str[1]}')
            print(f'n: {n_str[0]} +- {n_str[1]}')
            print(f'\u03C7^2: {round(goodness,2)}')
            print('-------------------------------------')
           
        return result
    
    # private Geraden Funktion  der Form f(x):=mx+n
    def __f(self,x):
        return self.n_val + self.m_val*x
        

    y_var = False      # Bool, ob y-Werte varianzgewichtet werden
    x_var = False      # Bool, ob x-Werte varianzgewichtet werden
    y_err = [0]
    x_err = [0]

    # Gebe y- und x-Fehler aus als Array falls noch kein Array
    def __get_error(self):
        if len(self.y_err) == 1:
            self.y_err = np.array([self.y_err[0]]*len(self.x_val))
        if len(self.x_err) == 1:
            self.x_err = np.array([self.x_err[0]]*len(self.x_val))
        if(self.y_err[0] == 0):
            self.y_err = [0]*len(self.x_val)
        if(self.x_err[0] == 0):
            self.x_err = [0]*len(self.x_val)
        return self.y_err,self.x_err


    # die textloc variable bestimmt die Stelle, an der sich die weiteren Infos im Graphen befinden
    textloc = 'upper right'


    #--Wichtig---------------------------
    # erstellt optionale Fehlerkurven
    def _s(self,val):
        try:
            return np.sqrt(self.m_err**2*val**2+self.n_err**2+2*self.Vmn*val)
        except RuntimeWarning:
            return 0
      

    #OPTIONAL
    #ändere die Größe des ausgegebenen Plots
    plotsize = (6,4)

    #OPTIONAL
    #ändere das Aussehen der Errorbars
    errbar = [5,5,1,1,'o'] # marker, caps, eline, markerwidth
    ANCH = 7

    #größe der Legende
    legendsize = 9
    legend_label = ['Geraden-Fit','Messwerte']
   
    # die Variablen der Limits des Diagramms
    ylim = (0,0)
    xlim = (0,0)

    # Setze die Ticks der Achsen
    xticks = 0
    yticks = 0

    # Rotation der Achsenbeschriftung
    xrotation = 0
    yrotation = 0

    # ändere die Farben im Diagramm
    colors = ['tab:red', 'black', 'black', 'steelblue']
    dpi = 300

    grid = False   # falls True, dann wird ein gitter im Hintergrund des plots eingefügt
    
    #---WICHTIG!!!!!!!!!!!!---------------------------------------------------
    # hiermit kann ein optionaler Plot erstellt werden
    def plot(self, title = 'title', xlabel = 'x_achse', ylabel = 'y_achse', err=True, legend = True, infos = False ,name='',hide = False, scale = 0.7, grid = ''):
        # result ist das dictionary, welches bei einem fit ausgegeben wird, bei err = True werden fehlerkurven angezeigt, bei infos werden zusätzliche Infos ausgegeben, 
        # bei hide = True wird die fit-gerade unterdrückt, scale gibt die Größe beim LaTeX Dokument an
        
        
        # Erstellt das Diagramm
        plt.style.use('default') # verhindert, dass Fehler bei der Anzeige entstehen
        try:
            plt.style.use(self.style)
        except:
            print(f'error: konnte den plot style in der Bibliothek nicht finden, Default: {self.style}. Es wird empfohlen, das Paket scienceplots zu installieren')
            plt.style.use('default')
        self._size()
        
        plt.rcParams['figure.dpi'] = 120
        fig, ax = plt.subplots(figsize=self.plotsize)
        
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        # setze die limits der achsen
        if self.ylim != (0,0):
            ax.set_ylim(self.ylim)
        if self.xlim != (0,0):
            ax.set_xlim(self.xlim)
        
        #setze die ticks der achsen
        try:
            if self.xticks != 0:
                plt.xticks(self.xticks)
            if self.yticks != 0:
                plt.yticks(self.yticks)
        except:
            print('error: konnte nicht ticks setzen')
        
        ax.tick_params(axis='x', labelrotation=self.xrotation)
        ax.tick_params(axis='y', labelrotation=self.yrotation)
        
        # Erstelle Errorbar 
        self.__get_error()
        ax.errorbar(self.x_val, self.y_val,color=self.colors[0],marker=self.errbar[4],markersize=self.errbar[0],linestyle='',zorder=10,
            yerr=self.y_err, xerr=self.x_err,label=self.legend_label[1],capsize=self.errbar[1], elinewidth=self.errbar[2], markeredgewidth=self.errbar[3])
       
        
        #bekomme momentane xlim
        left, right = ax.get_xlim()
        x_axis = np.linspace(left,right,20)

        #ax.plot(self.x_val, self.__f(self.x_val),color=self.colors[1],label=self.legend_label[0])
        if hide == False:
            ax.plot(x_axis, self.__f(x_axis),color=self.colors[1],label=self.legend_label[0],zorder=1)
        self.legend_label[0] = 'Geraden-Fit'

        if self.detail == True and self.HIDE == False:
            print('f(x[0]): +-', self.__f(self.x_val[0]).round(2))
            print('f(x_letztes): +-', self.__f(self.x_val[(len(self.x_val)-1)]).round(2))
            print('----------------------------')

        # Erstelle Fehlerkurven um die Geraden herum, falls err==True gesetzt wurde
        if(err==True and hide == False):
            ax.plot(x_axis, self.__f(x_axis)+self._s(x_axis),'--',color=self.colors[2],zorder=1,alpha=0.8,lw=0.9,label='Fehlerkurve')
            ax.plot(x_axis, self.__f(x_axis)-self._s(x_axis),'--',color=self.colors[2],zorder=1,alpha=0.8,lw=0.9)

            # Fülle den Raum zwischen beiden Fehlerkurven mit einer Farbe
            plt.gca().fill_between(x_axis, self.__f(x_axis)+self._s(x_axis), self.__f(x_axis)-self._s(x_axis),
             alpha=0.2,color=self.colors[3])


            # Gebe den Anfangs-, Mittleren- und Endwert der Fehlerkurve bei Bedarf aus, damit man besser abzeichnen kann
            if self.detail == True and self.HIDE == False:
                print('s(x[0]): +-', self._s(self.x_val[0]).round(2))
                print('s(x_mittel): +-', self._s(self.x_mittel).round(2)) 
                print('s(x_letztes): +-', self._s(self.x_val[(len(self.x_val)-1)]).round(2))

        # füge manuelle Plots hinzu:
        try:
            if self.custom_multi_array != 0:
                for i in range(np.shape(self.custom_plot_x)[1]):
                    ax.plot(self.custom_plot_x[:,i],self.custom_plot_y[:,i],label=self.custom_label[i],color = self.custom_colors[i],zorder=2)
            else:
                ax.plot(self.custom_plot_x,self.custom_plot_y,label=self.custom_label,color = self.custom_colors,zorder=2)
        finally:
            
            # setze xlim zurück
            ax.set_xlim((left,right))

            # Erstelle einen Kasten mit weiteren Infos im Diagramm
            if infos == True:
                at = self.AnchoredText(f'Achsenabschnitt: {self.n_val} $\pm$ {self.n_err} \n Steigung: {self.m_val} $\pm$ {self.m_err}',
                loc=self.textloc,prop=dict(size=self.ANCH))
                ax.add_artist(at)
            if legend == True:
                #---Löscht Fehlerbalken aus Legende---
                handles, labels = ax.get_legend_handles_labels()
                handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]

                ax.legend(handles, labels,frameon=True,prop={'size': self.legendsize})


            if grid != '':
                self.grid = grid
                
            if self.grid == True:
                ax.set_axisbelow(True)
                ax.grid(linestyle='--')
                
            if name != '':
                savefig(name,dpi=self.dpi,scale=scale)
               
            
            #plt.show()
            return ax

    # kann manuell zusätzlichen Plot hinzufügen
    custom_plot_x = 0
    custom_plot_y = 0
    custom_multi_array = 0
    custom_label = ['label']
    custom_colors = ['tab:green','tab:purple','tab:orange']
    def add_plot(self,x,y,label = '',colors = ''):
        if np.shape(x) == np.shape(y):
        
            if label != '':
                self.custom_label = label

            if colors != '':
                self.custom_colors = colors

            try:
                self.custom_plot_x = np.transpose(np.array(x))
                self.custom_plot_y = np.transpose(np.array(y))
            except:
                print('add_plot error')

            try:
                self.custom_multi_array = np.shape(self.custom_plot_x)[1]
                if label == '':
                    self.custom_label = ['label'] * self.custom_multi_array
            except:
                if colors == '':
                    self.custom_colors = 'tab:green'
                return
        else:
            print('x und y müssen diesselben Dimensionen haben')



#-------------------------------------------------------------------------------------------
#--------------------FÜGE-MEHRERE-GRAPPHEN-IM-SELBEN-DIAGRAMM-EIN---------------------------
#-------------------------------------------------------------------------------------------
# Lineare Funktion y = mx+n
def _linear(x, result):
    m = result['m']
    n = result['n']
        
    return m*x+n
    
def multiplot(result, title = 'Titel', xlabel = 'x-Achse', ylabel = 'y-Achse', color = ['tab:red', 'tab:green', 'tab:blue', 'tab:orange', 'tab:cyan'] , name = None, scale = 0.7, figsize = (7, 5.5), fontsize = 16, legendsize = 11, xrotation = 0, yrotation = 0, 
             custom = False, errbar = [7,5,1,1], symbols = ['x', 'o', 'v'], linestyle = '-'):
    
    def _size():
        BIG = fontsize 
        SMALL = fontsize * 0.6
        MID = fontsize * 0.75
        plt.rc('font', size=MID)          # controls default text sizes
        plt.rc('axes', titlesize=BIG)     # fontsize of the axes title
        plt.rc('axes', labelsize=MID)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL)    # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL)    # legend fontsize
        plt.rc('figure', titlesize=BIG)  # fontsize of the figure title
         
    if custom == False:   
        _size()
    
    
    ## kontrolliert, ob result ein dict ist, falls ja, wird es zu einer liste, damit der code auch für mehrere Elemente funktioniert
    if type(result) == dict:
        result = [result]
    if isinstance(color, str):
        color = [color]
    
    n = len(result)    # Anzahl der Fits
    label = [0]*n
    for ind, res in enumerate(result):
        label[ind] = res['name']
    
    fig, ax = plt.subplots(figsize = figsize)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    
    for i in range(n):
        x = result[i]['x_vals']
        y = result[i]['y_vals']
        xerr = result[i]['xerr']
        yerr = result[i]['yerr']
        color_ind = i % len(color)    # creates color cycle
        marker_ind = i % len(symbols)   # creates symbol cycle of errorbars
        
        #ax.plot(x, _linear(x, result[i]), color = color[color_ind])
        errorbar(ax, x, y, yerr, xerr, label = label[i], color = color[color_ind], marker = symbols[marker_ind], zorder = 2, errbar = errbar)
        
    xlim = ax.get_xlim()                                     # get current limits on x-axis
    x = np.linspace(xlim[0], xlim[1], 2)                     # mache neues Array mit xlim als Grenzen
    
    for i in range(n):
        color_ind = i % len(color)   
        ax.plot(x, _linear(x, result[i]), color = color[color_ind], zorder = 1, linestyle = linestyle)
        
    ax.set_xlim(xlim)           #setze xlim zurück, damit die Geraden über das ganze Diagramm gehen
    
    ax.tick_params(axis='x', labelrotation = xrotation)
    ax.tick_params(axis='y', labelrotation = yrotation)
    
    legend(ax, size = legendsize, anchor = (1.01, 1))
    
    if name != None and name != '':
        savefig(name = name, scale = scale)
        print(f'Plot {name} erfolgreich gespeichert')
        
    return ax
    
