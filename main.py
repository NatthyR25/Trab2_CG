from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from Objeto3D import *
import copy
import math

o:Objeto3D
o2:Objeto3D
o3:Objeto3D 

def init():
    global o
    global o2
    global o3
    global centroid1
    global centroid2
    global frameTime
    global associa
    global isVMoved
    isVMoved = []
    frameTime = 50
    centroid1 = Ponto(1000000, 1000000, 1000000)
    centroid2 = Ponto(1000000, 1000000, 1000000)
    glClearColor(0.5, 0.5, 0.9, 1.0)
    glClearDepth(1.0)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    o = Objeto3D()
    o.LoadFile('dude.obj')
    o2 = Objeto3D()
    o2.LoadFile('Porsche_911_GT2.obj')
    o3 = Objeto3D()
    
    o.DivideQuadrado()
    o2.DivideQuadrado()
    Associa()
    o3 = copy.deepcopy(o)
    createIsVMoved()
    #copiaVertices()
    #calculaCentroides()
    
    DefineLuz()
    PosicUser()


def DefineLuz():
    # Define cores para um objeto dourado
    luz_ambiente = [0.4, 0.4, 0.4]
    luz_difusa = [0.7, 0.7, 0.7]
    luz_especular = [0.9, 0.9, 0.9]
    posicao_luz = [2.0, 3.0, 0.0]  # PosiÃ§Ã£o da Luz
    especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0

    glEnable(GL_COLOR_MATERIAL)

    #Habilita o uso de iluminaÃ§Ã£o
    glEnable(GL_LIGHTING)

    #Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luz_ambiente)
    # Define os parametros da luz nÃºmero Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT, GL_SPECULAR, especularidade)

    # Define a concentraÃ§Ã£oo do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado serÃ¡ o brilho. (Valores vÃ¡lidos: de 0 a 128)
    glMateriali(GL_FRONT, GL_SHININESS, 51)

def PosicUser():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Configura a matriz da projeção perspectiva (FOV, proporção da tela, distância do mínimo antes do clipping, distância máxima antes do clipping
    # https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluPerspective.xml
    gluPerspective(60, 16/9, 0.01, 50)  # Projecao perspectiva
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #Especifica a matriz de transformação da visualização
    # As três primeiras variáveis especificam a posição do observador nos eixos x, y e z
    # As três próximas especificam o ponto de foco nos eixos x, y e z
    # As três últimas especificam o vetor up
    # https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml
    gluLookAt(-2, 6, -8, 0, 0, 0, 0, 1.0, 0)

def DesenhaLadrilho():
    glColor3f(0.5, 0.5, 0.5)  # desenha QUAD preenchido
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glEnd()

    glColor3f(1, 1, 1)  # desenha a borda da QUAD
    glBegin(GL_LINE_STRIP)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glEnd()

def DesenhaPiso():
    glPushMatrix()
    glTranslated(-20, -1, -10)
    for x in range(-20, 20):
        glPushMatrix()
        for z in range(-20, 20):
            DesenhaLadrilho()
            glTranslated(0, 0, 1)
        glPopMatrix()
        glTranslated(1, 0, 0)
    glPopMatrix()

def DesenhaCubo():
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslated(0, 0.5, 0)
    glutSolidCube(1)

    glColor3f(0.5, 0.5, 0)
    glTranslated(0, 0.5, 0)
    glRotatef(90, -1, 0, 0)
    glRotatef(45, 0, 0, 1)
    glutSolidCone(1, 1, 4, 4)
    glPopMatrix()

def copiaVertices():
    for i in range(len(o.faces)):
        for j in o.faces[i]: 
            for a in range(len(o.faces)):
                for b in range(len(o.faces[a])): #Ainda bem que é O((n+3)^2) e não O(n^4)
                    if j == o.faces[a][b] and i != a: #j e o.faces[a][b] são os valores que correspondem a indices na lista de vertices
                        # i e a são indices do array de faces
                        v = o.vertices[j]
                        o.vertices.append(Ponto(v.x, v.y, v.z))
                        o.faces[a][b] = len(o.vertices) - 1
                    

def calculaCentroides():
    global centroid1 
    maior1 = Ponto(0,0,0)
    menor1 = Ponto(0,0,0) 
    global centroid2
    maior2 = Ponto(0,0,0)
    menor2 = Ponto(0,0,0)

    for i in o.vertices:

        if i.x > maior1.x:
            maior1.x = i.x
        if i.x < menor1.x:
            menor1.x = i.x

        if i.y > maior1.y:
            maior1.y = i.y
        if i.y < menor1.y:
            menor1.y = i.y

        if i.z > maior1.z:
            maior1.z = i.z
        if i.z < menor1.z:
            menor1.z = i.z

    for i in o2.vertices:

        if i.x > maior2.x:
            maior2.x = i.x
        if i.x < menor2.x:
            menor2.x = i.x

        if i.y > maior2.y:
            maior2.y = i.y
        if i.y < menor2.y:
            menor2.y = i.y

        if i.z > maior2.z:
            maior2.z = i.z
        if i.z < menor2.z:
            menor2.z = i.z
    
    X = (maior1.x - menor1.x)/2 + menor1.x
    Y = (maior1.y - menor1.y)/2 + menor1.y
    Z = (maior1.z - menor1.z)/2 + menor1.z
    centroid1 = Ponto(X, Y, Z)

    X = (maior2.x - menor2.x)/2 + menor2.x
    Y = (maior2.y - menor2.y)/2 + menor2.y
    Z = (maior2.z - menor2.z)/2 + menor2.z
    centroid2 = Ponto(X, Y, Z) 


def Associa(): 
    #A Lista a seguir será preenchida por 
    global associa
    associa = []
    #As listas a seguir serão preenchidas por [Indice da face no array de faces, Distância do centroide da face em relação ao centroide do objeto]
    associa1 = []
    associa2 = []
    
    for i in range(len(o.faces)):
        associa1.append(None) #Abre espaço na lista, None é apenas para preecher tal espaço temporáriamente
        p1 = o.vertices[o.faces[i][0]]
        p2 = o.vertices[o.faces[i][1]] #Pega todos os pontos do triângulo
        p3 = o.vertices[o.faces[i][2]]
        centroidT = Ponto(math.floor((p1.x + p2.x + p3.x)/3), math.floor((p1.y + p2.y + p3.y)/3), math.floor((p1.z + p2.z + p3.z)/3)) #Calcula o centróide do triângulo
        #A distância entre o centróide do objeto e o centróide do triângulo é calculada abaixo:        
        distanciaCentroides = math.sqrt((centroidT.x - centroid1.x)**2 + (centroidT.y - centroid1.y)**2 + (centroidT.z - centroid1.z)**2)
        temp = i #Temp vai ser usado para modificar o associa1 depois
        for j, val in enumerate(associa1):
            if val == None:
                temp = j
                break
            elif val[1] >= distanciaCentroides:     #O bloco desse garante que a lista associa1 esteja ordenada pelas variáveis distanciaCentroides
                temp = j
                break
        if associa1[temp] == None:
            associa1[temp] = [i, distanciaCentroides]
        else:
            associa1.insert(temp, [i, distanciaCentroides])
            if associa1[-1] == None:
                associa1.pop(-1)
    
    for i in range(len(o2.faces)):
        associa2.append(None) #Abre espaço na lista, None é apenas para preecher tal espaço temporáriamente
        p1 = o2.vertices[o2.faces[i][0]]
        p2 = o2.vertices[o2.faces[i][1]] #Pega todos os pontos do triângulo
        p3 = o2.vertices[o2.faces[i][2]]
        centroidT = Ponto(math.floor((p1.x + p2.x + p3.x)/3), math.floor((p1.y + p2.y + p3.y)/3), math.floor((p1.z + p2.z + p3.z)/3)) #Calcula o centróide do triângulo
        #A distância entre o centróide do objeto e o centróide do triângulo é calculada abaixo:
        distanciaCentroides = math.sqrt((centroidT.x - centroid2.x)**2 + (centroidT.y - centroid2.y)**2 + (centroidT.z - centroid2.z)**2)
        temp = i #temp será o indíce que será usado para
        for j, val in enumerate(associa2):
            if val == None:
                temp = j
                break
            elif val[1] >= distanciaCentroides:     #O bloco desse garante que a lista associa2 esteja ordenada pelas variáveis distanciaCentroides
                temp = j
                break
        if associa2[temp] == None:
            associa2[temp] = [i, distanciaCentroides]
        else:
            associa2.insert(temp, [i, distanciaCentroides])
            if associa2[-1] == None:
                associa2.pop(-1)

    if len(associa1) < len(associa2): #Esse trecho serve pra equalizar as listas associa1 e 2
        for i in range(len(associa1), len(associa2)):
            o.faces.append([])
            a = math.floor(len(associa1) * (i/len(associa2)))

            for j in o.faces[a]:
                v = o.vertices[j]
                o.vertices.append(Ponto(v.x, v.y, v.z))
                o.faces[-1].append(len(o.vertices) - 1)
            
            associa1.insert(a, [len(o.faces) - 1, associa1[a][1]])


    for i in range(len(associa1)):
        associa.insert(associa1[i][0], associa2[i][0])

def createIsVMoved():
    for i in range(len(o3.vertices)):
        isVMoved.append(False)


def Morph():
    global frameTime
    global associa
    global isVMoved

    for i in range(len(o3.vertices)):
        isVMoved[i] = False
    for i in range(len(associa)):
        for j in range(3):
            k = o3.faces[i][j] #o3.faces[i][j] == o.faces[i][j]
            if not (isVMoved[k]):
                v1 = o.vertices[k] # v1 recebe um objeto Ponto() que é um vértice do obj1
                v2 = o2.vertices[o2.faces[associa[i]][j]] # v2 recebe um objeto Ponto() que é um vértice do obj2
                v3 = o3.vertices[k]
                tempV = Ponto(v2.x - v1.x, v2.y - v1.y, v2.z - v1.z) #Temp é a diferença entre v1 e v2 A.K.A: v2 - v1 = temp
                tempV.x = tempV.x / frameTime #Divide temp pelo numero de frames da animação pra não ser instantânio
                tempV.y = tempV.y / frameTime
                tempV.z = tempV.z / frameTime
                o3.vertices[k] = Ponto(v3.x + tempV.x, v3.y + tempV.y, v3.z + tempV.z)
                isVMoved[k] = True
                



def desenha():
    DefineLuz()
    PosicUser()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)

    DesenhaPiso()
    #DesenhaCubo()    
    o.Desenha()
    o.DesenhaWireframe()
    o.DesenhaVertices()
    print("a")
    glutSwapBuffers()
    pass

def desenha2():
    DefineLuz()
    PosicUser()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)

    DesenhaPiso()
    #DesenhaCubo()    
    

    o2.Desenha()
    o2.DesenhaWireframe()
    o2.DesenhaVertices()
    print("b")

    glutSwapBuffers()
    pass

def desenha3():
    DefineLuz()
    PosicUser()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)

    DesenhaPiso()
    #DesenhaCubo()    
    

    o3.Desenha()
    o3.DesenhaWireframe()
    o3.DesenhaVertices()
    print("c") 

    glutSwapBuffers()
    Morph()
    pass

def teclado(key, x, y):
    o.rotation = (1, 0, 0, o.rotation[3] + 2)    
    o2.rotation = (1, 0, 0, o.rotation[3] + 2)
    o3.rotation = (1, 0, 0, o.rotation[3] + 2)

    glutPostRedisplay()
    pass

def teclado2(key, x, y):
    o.rotation = (1, 0, 0, o.rotation[3] + 2)  
    o2.rotation = (1, 0, 0, o.rotation[3] + 2) 
    glutPostRedisplay()
    pass

def main():
    glutInit(sys.argv)

    # Define o modelo de operacao da GLUT
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)

    
    # Especifica o tamnho inicial em pixels da janela GLUT
    glutInitWindowSize(640, 480)

    # Especifica a posição de início da janela
    glutInitWindowPosition(100, 100)

    # Cria a janela passando o título da mesma como argumento
    glutCreateWindow('Objeto1 - 3D')

    # Registra a funcao callback de redesenho da janela de visualizacao
    glutDisplayFunc(desenha)

    # Registra a funcao callback para tratamento das teclas ASCII
    glutKeyboardFunc(teclado)

    # Cria a janela passando o título da mesma como argumento
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(100 + 640, 100)
    glutCreateWindow('Objeto2 - 3D')
    glutDisplayFunc(desenha2)
    glutKeyboardFunc(teclado)

    glutInitWindowSize(640, 480)
    glutInitWindowPosition(50 + 640, 300)
    glutCreateWindow('Morph - 3D')
    glutDisplayFunc(desenha3)
    glutKeyboardFunc(teclado)

    # Função responsável por fazer as inicializações
    init()

    try:
        # Inicia o processamento e aguarda interacoes do usuario
        glutMainLoop()
    except SystemExit:
        pass

if __name__ == '__main__':
    main()
