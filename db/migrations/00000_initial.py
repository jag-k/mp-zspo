from pony.orm.migrations.operations import AddEntity
from pony.orm.migrations.virtuals import Discriminator, Required, Optional, PrimaryKey, VirtualEntity as Entity
from pony.orm import Json
from datetime import date

dependencies = []

operations = [
    AddEntity(Entity('Admin',  attrs=[
        PrimaryKey('id', int, auto=True), 
        Required('login', str, unique=True), 
        Optional('name', str), 
        Required('hash', str, unique=True)])),

    AddEntity(Entity('Settings',  attrs=[
        PrimaryKey('key', str), 
        Required('value', Json)])),

    AddEntity(Entity('Post',  attrs=[
        PrimaryKey('id', int, auto=True), 
        Required('title', str), 
        Optional('link', str), 
        Optional('description', str), 
        Required('date', date), 
        Optional('hidden', bool), 
        Required('content', str), 
        Discriminator('classtype', str, column='classtype')])),

    AddEntity(Entity('News', bases=['Post'], attrs=[
        Optional('image', str)])),

    AddEntity(Entity('Category',  attrs=[
        PrimaryKey('id', int, auto=True), 
        Required('name', str), 
        Optional('link', str), 
        Optional('hidden', bool)])),

    AddEntity(Entity('Block',  attrs=[
        PrimaryKey('id', int, auto=True), 
        Required('name', str), 
        Optional('link', str)])),

    AddEntity(Entity('Header',  attrs=[
        PrimaryKey('id', int, auto=True), 
        Required('name', str), 
        Optional('url', str)]))
]
