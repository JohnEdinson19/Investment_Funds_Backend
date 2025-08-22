# Documentación de Despliegue - BTG Pactual Investment Funds Backend

## Arquitectura de Despliegue

El backend está desplegado usando **Serverless Framework** que genera automáticamente templates de **AWS CloudFormation** para gestionar la infraestructura como código.

## Recursos AWS Desplegados

### Infraestructura Principal
- **AWS Lambda Function**: `btg-pactual-api-dev-api`
  - Runtime: Container Image (Python 3.11)
  - Memory: 512 MB
  - Timeout: 15 segundos
  - Variables de entorno configuradas

- **Amazon ECR Repository**: `serverless-btg-pactual-api-dev`
  - Almacena las imágenes Docker del backend
  - URL: `https://k3kbiwfs2k.execute-api.us-east-1.amazonaws.com`

### Despliegue Automatizado (GitHub Actions)
El proyecto incluye CI/CD automático que se ejecuta en:
- Push a rama `develop` → Deploy a stage `dev`
- Push a rama `main` → Deploy a stage `prod`

# Recursos AWS - BTG Pactual Investment Funds Backend

## Servicios AWS Utilizados

### 🚀 **AWS Lambda**
- **Función**: `btg-pactual-api-dev-api`
- **Runtime**: Container Image
- **Arquitectura**: x86_64
- **Memoria**: 512 MB
- **Timeout**: 15 segundos
- **Justificación**: Serverless computing para escalabilidad automática y costo-efectividad

### 🐳 **Amazon ECR (Elastic Container Registry)**
- **Repository**: `serverless-btg-pactual-api-dev`
- **Justificación**: Almacenamiento seguro de imágenes Docker con integración nativa a Lambda

### 🌐 **Amazon API Gateway (HTTP API)**
- **API ID**: `k3kbiwfs2k`
- **Tipo**: HTTP API (más económico que REST API)
- **Endpoints**: 
  - `ANY /` 
  - `ANY /{proxy+}`
- **URL**: `https://k3kbiwfs2k.execute-api.us-east-1.amazonaws.com`
- **Justificación**: Punto de entrada HTTP para el backend con throttling y caching automático

### 🔐 **AWS IAM (Identity and Access Management)**
- **Role**: `btg-pactual-api-dev-us-east-1-lambdaRole`
- **Políticas**: 
  - Ejecución básica de Lambda
  - Escritura a CloudWatch Logs
- **Justificación**: Principio de menor privilegio para seguridad

### 📊 **Amazon CloudWatch**
- **Log Group**: `/aws/lambda/btg-pactual-api-dev-api`
- **Métricas**: Duración, errores, invocaciones
- **Justificación**: Monitoreo y observabilidad del sistema

### ☁️ **AWS CloudFormation**
- **Stack**: `btg-pactual-api-dev`
- **Template**: Generado automáticamente por Serverless Framework
- **Justificación**: Infraestructura como código, versionado y reproducible

### 📦 **Amazon S3**
- **Bucket**: `btg-pactual-api-dev-serverlessdeploymentbucket-*`
- **Uso**: Almacena artefactos de deployment
- **Justificación**: Storage dureable para artefactos del pipeline

## Base de Datos Externa

### 🍃 **MongoDB Atlas**
- **Cluster**: `InvestmentCluster`
- **Justificación**: Base de datos NoSQL managed, alta disponibilidad, sin administración de servidores

## Regiones y Disponibilidad

- **Región Principal**: `us-east-1` (Virginia)
- **Justificación**: Menor latencia para usuarios, costos optimizados
- **Disponibilidad**: Multi-AZ automática en Lambda y API Gateway

## Consideraciones de Costo

- **Lambda**: Pay-per-request (sin costo cuando no se usa)
- **API Gateway HTTP**: Más económico que REST API
- **ECR**: Storage mínimo para imágenes
- **CloudWatch**: Solo logs necesarios
- **Estimado mensual**: ~$5-10 USD para tráfico bajo-medio

# Justificación de la Arquitectura - BTG Pactual Investment Funds Backend

## Decisiones Arquitectónicas

### 🎯 **Arquitectura Serverless**

**Decisión**: Usar AWS Lambda + API Gateway en lugar de EC2/ECS
**Justificación**:
- ✅ **Escalabilidad automática**: Lambda escala de 0 a miles de requests automáticamente
- ✅ **Costo-efectivo**: Pay-per-request, no hay costos cuando no se usa
- ✅ **Alta disponibilidad**: Multi-AZ automática sin configuración
- ✅ **Mantenimiento cero**: AWS gestiona el servidor, OS, patches
- ✅ **Ideal para APIs**: Perfecta para workloads de API REST

### 🐳 **Container Images en Lambda**

**Decisión**: Usar imágenes Docker en lugar de código zip
**Justificación**:
- ✅ **Consistencia**: Mismo entorno en desarrollo y producción
- ✅ **Flexibilidad**: Mejor control sobre dependencias y runtime
- ✅ **Tamaño**: Permite paquetes más grandes (hasta 10GB)
- ✅ **CI/CD**: Integración natural con pipelines Docker

### 🌐 **HTTP API vs REST API**

**Decisión**: Usar HTTP API de API Gateway
**Justificación**:
- ✅ **Costo**: 70% más económico que REST API
- ✅ **Performance**: Menor latencia
- ✅ **Simplicidad**: Menos configuración necesaria
- ✅ **Suficiente**: Cubre todos los requerimientos del proyecto

### 🍃 **MongoDB Atlas (External)**

**Decisión**: Base de datos externa managed
**Justificación**:
- ✅ **Simplicidad**: No gestionar infraestructura de DB
- ✅ **Escalabilidad**: Escala horizontalmente
- ✅ **Backup automático**: Respaldos y recovery incluidos
- ✅ **Performance**: Optimizado para aplicaciones modernas
- ✅ **JSON nativo**: Perfect fit para APIs REST

### ☁️ **Infrastructure as Code**

**Decisión**: CloudFormation via Serverless Framework
**Justificación**:
- ✅ **Reproducibilidad**: Infraestructura versionada y reproducible
- ✅ **Rollback**: Fácil rollback a versiones anteriores
- ✅ **Auditoría**: Todos los cambios están tracked
- ✅ **Consistencia**: Mismo setup en dev/staging/prod

### 🔄 **CI/CD con GitHub Actions**

**Decisión**: GitHub Actions para deployment automático
**Justificación**:
- ✅ **Integración nativa**: Con el repositorio de código
- ✅ **Gratis**: Para repositorios públicos y uso moderado
- ✅ **Flexibilidad**: Workflows customizables
- ✅ **Seguridad**: Secrets management integrado

## Patrones Arquitectónicos Aplicados

### 🏗️ **Microservices Pattern**
- Cada función Lambda es un microservicio independiente
- Separation of concerns
- Escalabilidad independiente

### 🔌 **API Gateway Pattern**
- Single point of entry
- Cross-cutting concerns (throttling, CORS, auth)
- Request/response transformation

### 🏭 **Factory Pattern**
- Container images como "factory" para instancias Lambda
- Consistent runtime environment

### 📋 **Configuration as Code**
- Infrastructure as Code con CloudFormation
- Environment variables externalizadas
- Secrets management

## Beneficios de la Arquitectura

### 💰 **Costo**
- **Pay-per-use**: Solo pagas cuando se ejecuta
- **No infraestructura idle**: Cero costo en inactividad
- **Managed services**: Reduces operational costs

### 🚀 **Performance**
- **Cold start optimizado**: Container images más rápidas
- **Auto-scaling**: Respuesta inmediata a picos de tráfico
- **Global edge**: API Gateway con CloudFront integration

### 🔒 **Seguridad**
- **Principle of least privilege**: IAM roles mínimos
- **Network isolation**: Lambda VPC opcional
- **Encryption**: At rest y in transit por defecto

### 🛠️ **Operabilidad**
- **Observabilidad**: CloudWatch logs/metrics automáticos
- **Monitoring**: Alertas y dashboards built-in
- **Debugging**: X-Ray tracing disponible

### 🔄 **Mantenibilidad**
- **Infrastructure as Code**: Changes tracked y auditables
- **Blue/Green deployments**: Via Lambda versions/aliases
- **Zero-downtime updates**: Rolling updates automáticas

## Limitaciones y Trade-offs

### ⚠️ **Consideraciones**
- **Cold starts**: ~2-3s en primera invocación (mitigado con container images)
- **Execution time limit**: 15 minutos máximo (suficiente para APIs)
- **Memory limit**: 10GB máximo (más que suficiente)
- **Vendor lock-in**: Específico a AWS (mitigado por containerización)