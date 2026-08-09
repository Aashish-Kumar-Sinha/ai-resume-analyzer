from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# -----------------------------
# Resume Table
# -----------------------------
class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    raw_text = Column(Text, nullable=False)
    ats_score = Column(Integer)
    matched_skills = Column(JSON)

    matches = relationship(
        "JobMatch",
        back_populates="resume",
        cascade="all, delete-orphan"
    )


# -----------------------------
# Job Description Table
# -----------------------------
class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    raw_text = Column(Text, nullable=False)

    matches = relationship(
        "JobMatch",
        back_populates="job_description_ref",
        cascade="all, delete-orphan"
    )


# -----------------------------
# Resume ↔ JD Match Table
# -----------------------------
class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False
    )

    jd_id = Column(
        Integer,
        ForeignKey("job_descriptions.id", ondelete="CASCADE"),
        nullable=False
    )

    match_percentage = Column(Integer)
    matched_skills = Column(JSON)
    missing_skills = Column(JSON)
    ai_feedback = Column(Text)

    resume = relationship(
        "Resume",
        back_populates="matches"
    )

    job_description_ref = relationship(
        "JobDescription",
        back_populates="matches"
    )