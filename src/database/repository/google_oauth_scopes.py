from sqlmodel import Session, select, update

from src.database.entity.google_oauth_scopes import GoogleOauthScopes


class GoogleOauthScopesRepository:
    def get(self, session: Session) -> GoogleOauthScopes | None:
        sql_stmt = select(GoogleOauthScopes)
        result = session.exec(sql_stmt).first()
        return result.hashed_scopes

    def update(self, session: Session, *, hashed_scopes: str) -> int:
        stmt = update(GoogleOauthScopes).values(hashed_scopes=hashed_scopes)
        num_of_modified = session.exec(stmt)
        session.commit()
        return num_of_modified

    def insert(self, session: Session, *, hashed_scopes: str) -> GoogleOauthScopes:
        scopes = GoogleOauthScopes(hashed_scopes=hashed_scopes)
        session.add(scopes)
        session.commit()
        session.refresh(scopes)
        return scopes
