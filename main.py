from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from Objeto3D import *
import copy

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
    frameTime = 50
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
    o3 = copy.deepcopy(o)
    calculaCentroides()

    Qtdfaces_1 = len(o.faces) #Tamanho do array
    Qtdfaces_2 = len(o2.faces)
    global biggerObj
    
    if Qtdfaces_1 < Qtdfaces_2:
        biggerObj = 1
    else:
        biggerObj = 0 
    
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
    global associa
    associa1 = []
    associa2 = []
    for i in range(len(o.faces)):
        temp = o.faces[i][0]
        temp2 = o.faces[i][1]
        temp3 = Ponto(abs(temp.x - temp2.x), abs(temp.y - temp2.y), abs(temp.z - temp2.z)) #temp3 = ponto1 - ponto2 (pontos do triangulo)
        temp2 = o.faces[i][2]
        temp2 = Ponto(abs(temp.x - temp2.x), abs(temp.y - temp2.y), abs(temp.z - temp2.z)) #temp2 = ponto1 - ponto3 (pontos do triangulo)
        temp2 = Ponto(abs(temp3.x + temp2.x), abs(temp.y - temp2.y), abs(temp.z - temp2.z)) #temp2 = ponto1 - ponto3 (pontos do triangulo)
        associa1.append()


def Morph():
    global biggerObj
    global frameTime
    i = 0
    k = 0
    if biggerObj == 0:
        while(i < len(o.faces)):
            print("z")
            for j in range(3): #Range pode ser 4 caso o morph seja com quadrados, se quiser podemos botar parametro la no Morph
                v1 = o.vertices[ o.faces[i][j] ] # v1 recebe um objeto Ponto() que é um vértice do obj1
                v2 = o2.vertices[ o2.faces[k][j] ] # v2 recebe um objeto Ponto() que é um vértice do obj2
                temp = Ponto(v2.x - v1.x, v2.y - v1.y, v2.z - v1.z) #Temp é a diferença entre v1 e v2 A.K.A: v2 - v1 = temp
                temp.x = temp.x / frameTime #Divide temp pelo numero de frames da animação pra não ser instantânio
                temp.y = temp.y / frameTime
                temp.z = temp.z / frameTime
                o3.vertices[ o.faces[i][j] ] = v1 + temp # ob3 recebe essa mudança
            i = i + 1
            k = k + 1
            if k >= len(o2.faces):
                k = 0
        print("d")

    else:
        while(i < len(o2.faces)):
            print("z")
            for j in range(3): #Range pode ser 4 caso o morph seja com quadrados, se quiser podemos botar parametro la no Morph
                v1 = o.vertices[ o.faces[i][j] ] # v1 recebe um objeto Ponto() que é um vértice do obj1
                v2 = o2.vertices[ o2.faces[i][j] ] # v2 recebe um objeto Ponto() que é um vértice do obj2
                temp = Ponto(v2.x - v1.x, v2.y - v1.y, v2.z - v1.z) #Temp é a diferença entre v1 e v2 A.K.A: v2 - v1 = temp
                temp.x = temp.x / 50 #Divide temp pelo numero de frames da animação pra não ser instantânio
                temp.y = temp.y / 50
                temp.z = temp.z / 50
                o3.vertices[ o.faces[i][j] ] = v1 + temp # ob3 recebe essa mudança
                v3 = o3.vertices[ o.faces[i][j] ]
                v3.x = v1.x + temp.x
                v3.y = v1.y + temp.y
                v3.z = v1.z + temp.z

            i = i + 1
            if i >= len(o.faces):
                o.faces.append(o.faces[k]) #Copia uma face dentro do array de faces, e cola no final do mesmo array, isso é pra aumentar o array
                o3.faces.append(o3.faces[k])
                #k, nesse caso, é usado para rastrear as faces do começo ao fim, independentemente de "i"
                for j in range(3):
                    v = o.vertices[o.faces[k][j]] #Copia os dados de um vértice j
                    temp = Ponto(v.x, v.y, v.z) #Cola dentro de uma cópia
                    o.vertices.append(temp) #Enfia a cópia no fim no array de vertices
                    v = o3.vertices[o3.faces[k][j]]
                    temp = Ponto(v.x, v.y, v.z)
                    o3.vertices.append(temp) #Faz o mesmo no Morph
                    o.faces[-1][j] = len(o.vertices) - 1
                k = k + 1
                
        print("d")


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
