# Makefile pour le programme d'anonymisation

# Compilateur
CXX = g++

# Options de compilation
CXXFLAGS = -Wall -Wextra -std=c++11

# Nom de l'exécutable et des répertoires
EXECUTABLE = exe/programme_anonymisation
SRCDIR = src
OBJDIR = obj

# Liste des fichiers source
SRCS = $(wildcard $(SRCDIR)/*.cpp)

# Liste des fichiers objets générés à partir des fichiers source
OBJS = $(patsubst $(SRCDIR)/%.cpp,$(OBJDIR)/%.o,$(SRCS))

# Règle par défaut : générer l'exécutable
all: $(EXECUTABLE)

# Règle pour générer l'exécutable à partir des fichiers objets
$(EXECUTABLE): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Règle pour générer les fichiers objets à partir des fichiers source
$(OBJDIR)/%.o: $(SRCDIR)/%.cpp
	@mkdir -p $(@D)  # Crée le répertoire de destination si nécessaire
	$(CXX) $(CXXFLAGS) -c -o $@ $<

# Nettoyer les fichiers générés lors de la compilation
clean:
	rm -rf $(OBJDIR) $(EXECUTABLE)

# Assurez-vous que "clean" n'est pas considéré comme une cible
.PHONY: clean
