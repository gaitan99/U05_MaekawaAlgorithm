# U05_MaekawaAlgorithm

El algoritmo de maekawa se trata de un algoritmo de exlusión mutua para sistemas distribuidos, el funcionamiento de este se basa en que cada nodo tiene unos nodos compañeros a los que le tiene que pedir permiso, hasta que todos ellos no le permitan entrar este no podrá acceder a la sección crítica, una vez haya accedido realizará lo que tenga que hacer y este informará a sus compañeros que sale de la sección crítica, ya que mientras el nodo esté dentro de la sección crítica sus nodos compañeros no podrán permitir a otros nodos entrar en la sección crítica.
  
  **Estados del nodo que quiere acceder:**
  
    -INIT : El nodo está en estado inicial y no está pendiente de que le acepten ninguna petición.
    -REQUEST : El nodo ha enviado una petición para entrar y está pendiente de que se la acepten.
    -HELD : El nodo se encuentra dentro de la sección crítica.
    -RELEASE: EL nodo abandona la sección crítica y avisa a sus compañeros.
  
**  Nodo como compañero:**

    -has_voted : Este flag nos indica si el nodo ha votado una petición.
          False: Nos indica que no ha votado ninguna petición y que puede gestionar nuevas peticiones.
          True : Acaba de votar una petición por tanto las nuevas peticiones que lleguen se encolarán para ser procesadas posteriormente
    -voted_request : Este guardará la petición por la que ha votado, de tipo message.
    -requested_queue : Cola de prioridad donde se encolarán las peticiones que no pueden ser atendidas en ese momento.
    
    
**  Referencias:**

  Para realizar la práctica he extraido información de los enlaces propuestos en el enunciado de la práctica:
  - https://www.geeksforgeeks.org/maekawas-algorithm-for-mutual-exclusion-in-distributed-system/
  - https://en.wikipedia.org/wiki/Maekawa%27s_algorithm
  - https://github.com/yvetterowe/Maekawa-Mutex
   
    
