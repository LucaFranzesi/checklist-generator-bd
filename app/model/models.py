#region ------- IMPORTS -------------------------------------------------------------------------------------

from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column

#endregion ---- IMPORTS -------------------------------------------------------------------------------------

#region ------- INIT ----------------------------------------------------------------------------------------

# Init base declarative class for SQL table
Base = declarative_base()

#endregion ---- INIT ----------------------------------------------------------------------------------------
#region ------- MODEL ---------------------------------------------------------------------------------------

class Checklist(Base):
    __tablename__ = 'Checklist'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    sections: Mapped[List['Section']] = relationship(back_populates='checklist')

class Section(Base):
    __tablename__ = 'Section'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    checklist_id: Mapped[int] = mapped_column(ForeignKey('Checklist.id'))
    checklist: Mapped['Checklist'] = relationship(back_populates='sections')
    checks: Mapped[List['Check']] = relationship(back_populates='section')

class Check(Base):
    __tablename__ = 'Check'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str] = mapped_column(nullable=False)
    parent_id: Mapped[int] = mapped_column(ForeignKey('Check.id'), nullable=True)
    section_id: Mapped[int] = mapped_column(ForeignKey('Section.id'))
    section: Mapped['Section'] = relationship(back_populates='checks')

#endregion ---- MODEL ---------------------------------------------------------------------------------------