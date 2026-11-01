# ShopFlow — Engineering architecture

Modular monolith

## 1. Architectural principles

The project will follow these principles:

1. Domain-Driven Design (DDD): Organize code around business domains.
2. Clean Architecture: Business logic must not depend on FastAPI, SQLAlchemy, or external infrastructure.
3. SOLID: Clear responsibilities and dependency boundaries.
4. Repository Pattern: Persistence abstraction for domain/application use cases.
5. DTO Pattern: Explicit request, response, and internal data contracts.
6. Dependency Injection: Dependencies managed through application composition.
7. ML Engineering separation: Training, experimentation, inference, and business integration remain distinct.
8. Modular Monolith: Independent modules with explicit interfaces, deployed as one application.
9. Testability: Domain, application, integration, API, and ML tests.
10. Production readiness: Configuration, migrations, logging, security, observability, and reproducible builds.

## 2. Proposed backend scaffold

This is the architectural structure I want to establish:

```
backend/
├── pyproject.toml
├── uv.lock
├── .python-version
├── alembic.ini
│
├── alembic/
│   ├── env.py
│   └── versions/
│
├── src/
│   └── shopflow/
│       ├── __init__.py
│       │
│       ├── core/
│       │   ├── config/
│       │   ├── security/
│       │   ├── exceptions/
│       │   ├── logging/
│       │   ├── middleware/
│       │   ├── database/
│       │   └── dependencies/
│       │
│       ├── shared/
│       │   ├── domain/
│       │   │   ├── base_entity.py
│       │   │   ├── aggregate_root.py
│       │   │   └── domain_event.py
│       │   ├── application/
│       │   ├── infrastructure/
│       │   └── types/
│       │
│       ├── modules/
│       │   │
│       │   ├── identity/
│       │   │   ├── domain/
│       │   │   │   ├── models/
│       │   │   │   ├── enums/
│       │   │   │   ├── value_objects/
│       │   │   │   ├── events/
│       │   │   │   └── repositories/
│       │   │   ├── application/
│       │   │   │   ├── dtos/
│       │   │   │   ├── interfaces/
│       │   │   │   ├── services/
│       │   │   │   └── use_cases/
│       │   │   ├── infrastructure/
│       │   │   │   ├── persistence/
│       │   │   │   └── repositories/
│       │   │   └── api/
│       │   │       ├── controllers/
│       │   │       ├── schemas/
│       │   │       └── dependencies/
│       │   │
│       │   ├── catalog/
│       │   ├── categories/
│       │   ├── inventory/
│       │   ├── pricing/
│       │   ├── customers/
│       │   ├── sellers/
│       │   ├── carts/
│       │   ├── orders/
│       │   ├── payments/
│       │   ├── promotions/
│       │   ├── recommendations/
│       │   └── analytics/
│       │
│       ├── ml/
│       │   ├── datasets/
│       │   ├── features/
│       │   ├── pipelines/
│       │   ├── models/
│       │   ├── training/
│       │   ├── evaluation/
│       │   ├── inference/
│       │   ├── explainability/
│       │   ├── registry/
│       │   └── monitoring/
│       │
│       ├── integrations/
│       │   ├── mlflow/
│       │   └── external_services/
│       │
│       ├── bootstrap/
│       │   ├── container.py
│       │   └── application.py
│       │
│       └── main.py
│
├── notebooks/
├── scripts/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── architecture/
│   ├── api/
│   └── ml/
│
└── configs/
```

The abbreviated module folders will receive their own complete internal structure according to their responsibilities.

Important distinction: Domain models are not SQLAlchemy models. Domain entities represent business concepts; infrastructure persistence models represent database records. Repositories translate between them. We should not introduce unnecessary abstractions for simple entities, but preserve this separation where it provides real value.

## 3. Frontend scaffold

The React application will follow a feature-oriented architecture rather than organizing everything into generic component folders.

```
frontend/
├── public/
├── src/
│   ├── app/
│   │   ├── providers/
│   │   ├── router/
│   │   ├── layouts/
│   │   └── config/
│   │
│   ├── features/
│   │   ├── auth/
│   │   │   ├── api/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── schemas/
│   │   │   └── types/
│   │   ├── catalog/
│   │   ├── inventory/
│   │   ├── customers/
│   │   ├── sellers/
│   │   ├── cart/
│   │   ├── checkout/
│   │   ├── orders/
│   │   ├── recommendations/
│   │   └── analytics/
│   │
│   ├── components/
│   │   ├── ui/
│   │   ├── shared/
│   │   └── data-display/
│   │
│   ├── hooks/
│   ├── lib/
│   ├── services/
│   ├── stores/
│   ├── types/
│   ├── utils/
│   └── styles/
│
├── tests/
├── package.json
└── vite.config.ts
```

## 4. ML engineering scaffold

The ML system deserves its own engineering discipline.

We will distinguish:

- Experimental notebooks.
- Production feature engineering.
- Training pipelines.
- Model evaluation.
- Model artifacts and versioning.
- Inference interfaces.
- Business-facing prediction services.
- Monitoring.

For example, a delivery prediction model should not know anything about HTTP requests or React. Its responsibility is to accept validated features and return predictions.

The application layer will integrate that capability into order management.

## 5. Architecture enforcement

I also want architectural quality to be measurable.

We will establish rules such as:

| Rule                 | Requirement                                            |
| -------------------- | ------------------------------------------------------ |
| Domain independence  | No FastAPI or SQLAlchemy imports                       |
| Dependency direction | Infrastructure depends inward, never the reverse       |
| Module boundaries    | No direct access to another module's private internals |
| API isolation        | Controllers delegate to application use cases          |
| DTO isolation        | API schemas are not domain entities                    |
| Repository ownership | Each module owns its persistence logic                 |
| ML isolation         | Training code does not run inside HTTP requests        |
| Database integrity   | Transactions for order and inventory operations        |
| Testing              | Business rules tested independently of infrastructure  |

Architecture tests should enforce the most important dependency rules automatically.

# 6. Formal project vision

I will establish the following as the project's initial architectural baseline.

# ShopFlow — Project Vision

**Repository:** `shopflow`

**Product:** Full-Stack E-Commerce Marketplace with Integrated Machine Learning

**Architecture:** Modular Monolith + Domain-Driven Design + Clean Architecture

**Status:** Approved architectural direction

## 1. Product Vision

ShopFlow is a production-oriented e-commerce marketplace designed to demonstrate professional software engineering and machine learning engineering capabilities in one integrated product.

It provides a functional customer storefront, seller management, administrative operations, inventory management, order processing, and intelligent marketplace features.

Machine learning is integrated into actual business workflows rather than being implemented as disconnected experiments.

## 2. Core Technology Stack

### Frontend

- React
- TypeScript 7+
- Vite
- Tailwind CSS
- shadcn/ui
- TanStack Query
- React Hook Form
- Zod

### Backend

- Python (3.15 version also using lazy)
- FastAPI
- Pydantic
- SQLAlchemy 2
- Alembic
- PostgreSQL

### Python Tooling

- uv exclusively for Python dependency and environment management.
- uv lockfile for reproducible dependency resolution.
- No pip, Poetry, or Conda workflows.

### Machine Learning

- NumPy
- Pandas
- Polars
- Scikit-learn
- XGBoost
- CatBoost
- LightGBM
- PyTorch
- Statsmodels
- Implicit
- LightFM
- SHAP
- MLflow

Additional libraries should be introduced only when justified by a specific ML task.

### Infrastructure

- Docker
- Docker Compose
- GitHub Actions
- Pytest
- Vitest
- Ruff
- PostgreSQL

## 3. Product Modules

### Customer

- Authentication and account management.
- Product discovery.
- Search, filtering, and sorting.
- Product details.
- Shopping cart.
- Checkout.
- Order history.
- Wishlist.
- Personalized recommendations.

### Catalog

- Product CRUD.
- Categories and brands.
- Product variants.
- Product images.
- Pricing.
- Product availability.

### Inventory

- Stock management.
- Inventory adjustments.
- Stock movement history.
- Low-stock detection.
- Transaction-safe stock reservation.

### Orders

- Order creation.
- Order items.
- Order status lifecycle.
- Order history.
- Delivery tracking.
- Cancellation and refund workflows.

### Sellers

- Seller profiles.
- Product ownership.
- Seller inventory.
- Seller analytics.
- Seller order management.

### Administration

- User management.
- Role-based access control.
- Product and category management.
- Seller management.
- Order management.
- Promotions.
- Marketplace analytics.

## 4. ML Capabilities

### Product Recommendation

Benchmark popularity-based recommendation, collaborative filtering, ALS, LightFM, and neural recommendation approaches.

### Demand Forecasting

Compare statistical baselines, ARIMA/ETS, XGBoost, LightGBM, and CatBoost.

### Delivery Intelligence

Implement delivery ETA regression and late-delivery classification.

### Customer Intelligence

Implement customer segmentation and repurchase prediction.

### Model Engineering

Provide reproducible experiments, feature pipelines, temporal validation, hyperparameter tuning, model evaluation, explainability, versioning, and inference.

## 5. Dataset Strategy

Use the Brazilian Olist e-commerce dataset as the primary historical ML dataset.

Maintain a strict separation between:

- Historical data used for ML training.
- Live marketplace data stored in PostgreSQL.
- Application seed data.
- Synthetic demonstration records, explicitly identified as synthetic.

Historical transactions must not be treated as live inventory or real-time marketplace activity.

## 6. Architectural Requirements

Use a modular monolith with explicit business modules.

Each backend module should follow an appropriate structure:

- domain/models
- domain/enums
- domain/value_objects
- domain/repositories
- application/dtos
- application/interfaces
- application/services
- application/use_cases
- infrastructure/persistence
- infrastructure/repositories
- api/controllers
- api/schemas
- api/dependencies

Use Clean Architecture dependency direction, repository abstractions, dependency injection, explicit DTOs, and well-defined module interfaces.

Keep ML experimentation, training, evaluation, and inference separated.

The frontend should follow feature-oriented architecture with shared UI components and clear API integration boundaries.

## 7. Quality Requirements

- Production-quality validation and error handling.
- Secure authentication and authorization.
- Database constraints and migrations.
- Transaction-safe business operations.
- Unit, integration, API, architecture, and ML tests.
- Structured logging.
- Health and readiness endpoints.
- Reproducible model training.
- Documented API contracts.
- Automated CI.
- Docker Compose deployment.
- Environment-based configuration.
- No hardcoded secrets.
- No fake model performance or misleading analytics.

## 8. Completion Criteria

ShopFlow is considered complete only when:

1. The customer storefront works.
2. Authentication and authorization work.
3. Product, category, customer, seller, and inventory CRUD operations work.
4. Cart and order workflows work.
5. PostgreSQL persists application data correctly.
6. ML pipelines are reproducible and properly evaluated.
7. ML predictions are accessible through application APIs.
8. The frontend consumes the backend successfully.
9. Automated tests pass.
10. The entire system starts through Docker Compose.
11. Documentation allows another developer to clone, configure, run, and understand the application.

## 9. Engineering Objective

ShopFlow must demonstrate the ability to design, implement, test, deploy, and maintain a complete software product while applying sound machine learning engineering practices.

Prioritize working business functionality, measurable ML performance, maintainable architecture, and reproducibility over unnecessary technological complexity.

This is the baseline vision. The detailed implementation specification should expand it with database entities and relationships, API contracts, business workflows, feature definitions, ML acceptance thresholds, security requirements, and deployment checks.

My architectural recommendation: Keep the modular monolith strict, but pragmatic. We want professional boundaries without creating 40 abstractions for a simple CRUD operation. That balance is what will make ShopFlow both impressive and maintainable.
