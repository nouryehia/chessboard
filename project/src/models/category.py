from __future__ import annotations

from ...setup import db
from typing import Dict
from .models import course


class Category(db.Model):
    '''
    Represents a weighted category for a given course in the DB.\n
    Fields: \n
    id --> Category ID. Unique, primary key. \n
    name --> Name of the category. \n
    weight --> Weight of the category in grade. \n
    course_id --> Course that category is in. Foreign key. \n
    @author: tiffany-meng and ansomasu\n
    '''
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(course.id), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def restore(self) -> Category:
        self.is_deleted = False
        self.save()
        return self

    def save(self) -> None:
        """
        Upadate the object to the database.
        Params: None
        Returns: None
        """
        db.session.commit()

    def soft_delete(self) -> Category:
        """
        Marks a category as deleted without removing it from the database
        Params: None
        Returns: This category
        """
        self.is_deleted = True
        self.save()
        return self

    def to_json(self) -> Dict[str, str]:
        ret = {}
        ret['id'] = self.id
        ret['name'] = self.name
        ret['weight'] = self.weight
        ret['course_id'] = self.course_id
        return ret

    @staticmethod
    def create_category(cat_name: str, percent: float, course: int) -> None:
        '''
        Creates a new category object and add it to the database.
        Params:
        name - name of the assignment category
        percent - weight of the category in grade
        course - id of the course the assignment is in
        '''
        cat = Category(name=cat_name, weight=percent, course_id=course,
                       is_deleted=False)
        db.session.add(cat)
        db.session.commit()

    @staticmethod
    def delete_all_for_course(course: int) -> None:
        '''
        Soft-deletes all categories for a course.
        Params:
        course - id of the course the assignment is in
        '''
        category_list = Category.query.filter_by(course_id=course).all()
        for category in category_list:
            category.soft_delete()
        db.session.commit()

    @staticmethod
    def restore_all_for_course(course: int) -> None:
        '''
        Restores all deleted categories for a course.\n
        Params:
        course - id of the course to restore the categories for\n
        Returns: None\n
        '''
        category_list = Category.query.filter_by(course_id=course).all()
        for category in category_list:
            category.restore()
        db.session.commit()
