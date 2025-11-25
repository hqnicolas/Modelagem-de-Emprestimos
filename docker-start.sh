#!/bin/bash

# Script de inicialização Docker para Sistema de Análise de Crédito

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Sistema de Análise de Crédito - Docker Deploy            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para verificar se Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Docker não está instalado!${NC}"
        echo ""
        echo "Por favor, instale o Docker:"
        echo "  - Linux: https://docs.docker.com/engine/install/"
        echo "  - Mac: https://docs.docker.com/desktop/install/mac-install/"
        echo "  - Windows: https://docs.docker.com/desktop/install/windows-install/"
        exit 1
    fi
    echo -e "${GREEN} Docker encontrado: $(docker --version)${NC}"
}

# Função para verificar se Docker Compose está instalado
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}Docker Compose não está instalado!${NC}"
        echo ""
        echo "Por favor, instale o Docker Compose:"
        echo "  https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    if command -v docker-compose &> /dev/null; then
        echo -e "${GREEN} Docker Compose encontrado: $(docker-compose --version)${NC}"
        COMPOSE_CMD="docker-compose"
    else
        echo -e "${GREEN} Docker Compose encontrado: $(docker compose version)${NC}"
        COMPOSE_CMD="docker compose"
    fi
}

# Função para verificar arquivos necessários
check_files() {
    echo ""
    echo -e "${BLUE} Verificando arquivos necessários...${NC}"
    
    MISSING_FILES=()
    
    if [ ! -f "lgbm_model_optimized.pkl" ]; then
        MISSING_FILES+=("lgbm_model_optimized.pkl")
    fi
    
    if [ ! -f "scaler.pkl" ]; then
        MISSING_FILES+=("scaler.pkl")
    fi
    
    if [ ! -f "app.py" ]; then
        MISSING_FILES+=("app.py")
    fi
    
    if [ ! -f "requirements.txt" ]; then
        MISSING_FILES+=("requirements.txt")
    fi
    
    if [ ! -f "Dockerfile" ]; then
        MISSING_FILES+=("Dockerfile")
    fi
    
    if [ ! -f "docker-compose.yml" ]; then
        MISSING_FILES+=("docker-compose.yml")
    fi
    
    if [ ${#MISSING_FILES[@]} -gt 0 ]; then
        echo -e "${RED}❌ Arquivos faltando:${NC}"
        for file in "${MISSING_FILES[@]}"; do
            echo "   - $file"
        done
        echo ""
        echo "Por favor, certifique-se de que todos os arquivos estão presentes."
        exit 1
    fi
    
    echo -e "${GREEN}Todos os arquivos necessários estão presentes${NC}"
}

# Função para construir a imagem
build_image() {
    echo ""
    echo -e "${BLUE} Construindo imagem Docker...${NC}"
    echo "   Isso pode levar alguns minutos..."
    echo ""
    
    if $COMPOSE_CMD build; then
        echo ""
        echo -e "${GREEN}Imagem construída com sucesso!${NC}"
    else
        echo ""
        echo -e "${RED}Erro ao construir imagem${NC}"
        exit 1
    fi
}

# Função para iniciar os containers
start_containers() {
    echo ""
    echo -e "${BLUE} Iniciando containers...${NC}"
    echo ""
    
    if $COMPOSE_CMD up -d; then
        echo ""
        echo -e "${GREEN} Containers iniciados com sucesso!${NC}"
    else
        echo ""
        echo -e "${RED} Erro ao iniciar containers${NC}"
        exit 1
    fi
}

# Função para verificar status
check_status() {
    echo ""
    echo -e "${BLUE} Verificando status dos containers...${NC}"
    sleep 3
    
    if docker ps | grep -q "credit-analysis-system"; then
        echo -e "${GREEN} Container está rodando!${NC}"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo -e "${GREEN} Sistema de Análise de Crédito está ONLINE!${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo -e "${BLUE} Acesse a aplicação em:${NC}"
        echo "    http://localhost:8501"
        echo ""
        echo -e "${BLUE}Comandos úteis:${NC}"
        echo "   Ver logs:        $COMPOSE_CMD logs -f"
        echo "   Parar:           $COMPOSE_CMD down"
        echo "   Reiniciar:       $COMPOSE_CMD restart"
        echo "   Status:          $COMPOSE_CMD ps"
        echo ""
    else
        echo -e "${RED}Container não está rodando${NC}"
        echo ""
        echo "Verifique os logs com: $COMPOSE_CMD logs"
        exit 1
    fi
}

# Função principal
main() {
    echo ""
    echo "Verificando pré-requisitos..."
    echo ""
    
    check_docker
    check_docker_compose
    check_files
    
    stop_existing
    build_image
    start_containers
    check_status
}

# Executar função principal
main
