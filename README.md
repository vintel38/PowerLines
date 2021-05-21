# Power Lines Detection - Détection de lignes électriques

Ce répertoire est dédié à la réutilisation des résultats du papier [C. Pan, X. Cao and D. Wu, "Power line detection via background noise removal," 2016 IEEE GlobalSIP](https://ieeexplore.ieee.org/document/7905967). Le papier en question dévoile une technique nouvelle pour repérer des lignes électriques sur une image. Ce problème, qui peut paraître anodin, est en réalité d'une complexité assez surprenante. Effectivement, une ligne électrique ne comporte pas de caractéristiques géométriques intrinsèque sur laquelle on pourrait utiliser les techniques de détection d'objets classiques. Les conditions d'orientations, de luminosité, de contraste, de fond d'écran peuvent également énormément varier en extérieur rendant la tâche plus complexe et mettant de côté les techniques de segmentation traditionnelles. La technique évoquée ici transforme radicalement le cliché original vers une image qui garde une marque uniquement des arêtes présentes dans la photo. En utilisant la technique des filtres orientables [(Freeman, MIT 1991)](http://people.csail.mit.edu/billf/publications/Design_and_Use_of_Steerable_Filters.pdf), on peut alors améliorer la qualité et la signification de chaque arête. Un réseau de neurones CNN classique réalise alors la classification des pixels selon qu'ils appartiennent à un câble ou non. Ensuite, la technique de Transformée de Hough permet de lier les pixels qui appartiennent à une même ligne pour reconstituer la ligne électrique recherchée. La technique utilisée, mais également les distances prises avec l'article seront discutées dans la suite. 

## I ) Intérêt de la technologie

La détection de lignes électriques est un sujet d'actualité comme il permettra dans le futur d'effectuer l'inspection d'installations électriques sur de longues distances de manière totalement automatisée et sécurisée. En effet, la qualité et l'état de ces lignes conditionnent les capacités de distribution de réseaux d'électricité qui sont des infrastructures vitales d'un pays. Bon nombre d'articles scientifiques sont aujourd'hui dédiés à cette technique sous le nom de Power Line Detection (PLD) qui essaie d'exploiter les capacités du Machine Learning pour identifier et localiser plus facilement sur une image une ligne électrique quel que soit le fond d'écran. En effet, les réseaux de convolution permettent désormais de synthétiser des informations graphiques spatiales pour réduire la complexité des phases de traitement et améliorer l'extraction d'informations d'une image. 

Image Initiale             |  Image Détectée
:-------------------------:|:-------------------------:
<img src="https://github.com/vintel38/FreemanMIT1991/blob/main/images/sky.png" width="300" /> | <img src="https://github.com/vintel38/FreemanMIT1991/blob/main/images/sky_detected.png"  width="300" />
Images issues de Pan 2016  


## II ) L'extraction des arêtes orientées

L'extraction des contours d'une image est à l'origine de nombreux traitements graphiques du domaine de la vision informatique (Computer Vision). La technique la plus connue pour extraire des contours reste aujourd'hui [Canny Edge Detector](https://docs.opencv.org/master/da/d22/tutorial_py_canny.html) comme elle calcule rapidement et simplement la position et l'orientation des arêtes avec un coût de calcul relativement mesuré. Cependant, pour des objets fins, Canny retourne un contour pour chaque variation de lumière alors que pour un trait fin, il pourrait être intéressant de n'avoir qu'un seul contour. D'autre part, aucun contrôle n'est disponible sur l'orientation des arêtes et les premiers calculs ont montré des résultats moins qu'intéressants. Le sujet de la thèse de [Freeman](http://people.csail.mit.edu/billf/publications/Design_and_Use_of_Steerable_Filters.pdf) est de développer des bases de filtres gaussiens qui une fois combinés avec des fonctions d'interpolations produisent des filtres graphiques qui, par convolution avec les images, retournent toutes les arêtes proches d'une orientation donnée. 

Image Initiale            |  Image Filtrée
:-------------------------:|:-------------------------:
<img src="https://github.com/vintel38/FreemanMIT1991/blob/main/images/albert.png" width="300" /> | <img src="https://github.com/vintel38/FreemanMIT1991/blob/main/images/einstein.png"  width="300" />
Images issues de Freeman 1991

La première étape, comme stipulé dans l'article, est d'améliorer les contours avant de procéder au traitement graphique. La technique du papier menant à une publication difficilement lisible, on se rabat sur une technique maîtrisée, à savoir la soustraction du bruit gaussien que l'on peut trouver dans le fichier Canny.py. A partir d'un filtre gaussien classique, elle calcule un flou de l'image qu'elle soustrait à l'image originale pour obtenir l'image aux contours accentués. 

Ensuite, on passe à l'extraction orientée des arêtes. On utilise alors la technique des filtres gaussiens orientés. Si l'on souhaite ne détecter que des lignes électriques selon une direction approximative, on peut se contenter d'appliquer une seule combinaison de filtres gaussiens selon la direction correspondante pour que seules les arêtes selon cette direction soient mises en valeur en sortie. C'est ce qui a été fait dans le cadre de ce répertoire : pour des photos avec des lignes électriques verticales, une seule combinaison de filtres orientés a été utilisée dans laquelle les fonctions d'interpolation utilisaient un angle de pi/2 (dans le répère trigonométrique). D'autre part, l'article de Pan et al fait référence à des filtres gaussiens orientés du troisième ordre sans donner l'expression de la base des filtres. Comme les expressions littérales d'une base de filtres gaussiens orientés sont plus facilement disponibles dans la littérature et conviennent aux besoins de ce projet, ce sont ceux-ci qui ont été utilisés pour réaliser l'extraction des arêtes en privilégiant celles selon la verticale. 

Image Initiale            |  Image Filtrée
:-------------------------:|:-------------------------:
<img src="https://github.com/vintel38/PowerLines/blob/main/images/20210507_133045_001_edge.jpg" width="300" /> | <img src="https://github.com/vintel38/PowerLines/blob/main/images/20210507_133045_001_edge_steered.jpg"  width="300" />

## III ) Classification des pixels

Une fois que les arêtes verticales ont été extraites de l'image, on peut commencer à classifier celles qui font véritablement partie d'un objet type câble. Le réseau de neurones est reproduit à l'identique avec la bibliothèque Tensorflow dans le langage Python. Les morceaux d'images sont découpés depuis une image puis étiquetés avec un programme développé pour l'occasion (CropCable.py et CropNoise.py). Ensuite, les quelques 2000 images annotées sont chargées dans le programme Tensorflow (voir le notebook PowerLine.ipynb) pour réaliser l'entraînement du modèle. Comme annoncé par l'article, l'overfitting survient très rapidement comme le modèle a beaucoup de degré de liberté, mais trouve finalement assez peu d'informations dans le jeu de données d'entraînement. Plus d'annotations sont nécessaires ainsi que de l'augmentation de données pour pallier ce problème. Au bout de 3 epochs, on peut arrêter l'entraînement du modèle dont la précision en classification atteint 96%. La stagnation de la précision ainsi qu'une perte sur le jeu de validation supérieure à celle sur le jeu d'entraînement sont des exemples criants pour l'overfitting. 

Pixels Câble            |  Pixels non-Câble
:-------------------------:|:-------------------------:
<img src="https://github.com/vintel38/PowerLines/blob/main/images/1%20(1).jpeg" width="300" /> | <img src="https://github.com/vintel38/PowerLines/blob/main/images/0%20(1).jpeg"  width="300" />
<img src="https://github.com/vintel38/PowerLines/blob/main/images/1%20(2).jpeg" width="300" /> | <img src="https://github.com/vintel38/PowerLines/blob/main/images/0%20(2).jpeg"  width="300" />
<img src="https://github.com/vintel38/PowerLines/blob/main/images/1%20(3).jpeg"  width="300" /> | <img src="https://github.com/vintel38/PowerLines/blob/main/images/0%20(4).jpeg"  width="300" />

## IV ) Reconstruction des lignes

L'article évoque une technique avancée de Hough Transform. Cependant, l'article qui y fait référence est loin d'être lisible. On choisit donc la fonction HoughLinesP du module OpenCV pour réaliser cette opération. Si l'on s'attarde sur la description de cette fonction, on peut voir qu'elle est très similaire à celle de GPPHT de l'article ce qui conforte le choix. Comme on peut voir dans l'image de sortie du CNN qu'il reste du bruit, on utilise des valeurs très fortes pour le nombre de pixels nécessaire pour générer une ligne minLineLength ce qui supprime tout le bruit et ne garde uniquement que les lignes électriques. Avec l'utilisation des techniques de l'article scientifique Pan 2016, la détection de lignes électriques est désormais facilement réalisable avec un minimum de connaissances en Machine Learning. 

Image Initiale            |  Image Détectée
:-------------------------:|:-------------------------:
<img src="https://github.com/vintel38/PowerLines/blob/main/images/20210507_133045_001_edge.jpg" width="300" /> | <img src="https://github.com/vintel38/PowerLines/blob/main/images/20210507_133045_001_dyn.jpg"  width="300" />


VA 20/05/2021