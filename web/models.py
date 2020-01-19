from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TranslationStatus(db.Model):
    __tablename__ = 'translations_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(40))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_onupdate=db.func.now())

    translations = db.relationship('Translation', back_populates='status')

    def __repr__(self):
        return f'<TranslationStatus id: "{self.id}", status: "{self.status}">'


class Language(db.Model):
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_onupdate=db.func.now())

    def __repr__(self):
        return f'<Language id: "{self.id}", language: "{self.language}">'


class Translation(db.Model):
    __tablename__ = 'translations'

    uid = db.Column(db.String(20), primary_key=True)
    source_language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    input_text = db.Column(db.String(50))
    target_language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    output_text = db.Column(db.String(50))
    status_id = db.Column(db.Integer, db.ForeignKey('translations_status.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_onupdate=db.func.now())

    status = db.relationship('TranslationStatus', back_populates='translations')
    source_language = db.relationship('Language', foreign_keys=[source_language_id], backref='source_lang_translations')
    target_language = db.relationship('Language', foreign_keys=[target_language_id], backref='target_lang_translations')

    def __repr__(self):
        return f'<Translation uid: "{self.uid}", status: "{self.status}">'
