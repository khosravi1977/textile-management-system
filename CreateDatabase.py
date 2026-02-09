# -*- coding: utf-8 -*-
"""
اسکریپت ایجاد دیتابیس SQLite برای پروژه نساجی
"""

import sqlite3
import pandas as pd
import os
from datetime import datetime

class TextileDatabaseCreator:
    def __init__(self, db_path='TextileDB.db'):
        self.db_path = db_path
        self.conn = None
        
    def create_database(self):
        """ایجاد دیتابیس و جداول"""
        print("📦 در حال ایجاد دیتابیس فارسی...")
        
        try:
            # اتصال به دیتابیس (اگر وجود نداشت، ایجاد می‌شود)
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA encoding = 'UTF-8';")
            self.conn.execute("PRAGMA foreign_keys = ON;")
            
            # ایجاد جداول
            self._create_tables()
            
            # ایجاد ویوها
            self._create_views()
            
            # درج داده‌های اولیه
            self._insert_initial_data()
            
            print("✅ دیتابیس با موفقیت ایجاد شد!")
            
        except Exception as e:
            print(f"❌ خطا در ایجاد دیتابیس: {e}")
            raise
            
        finally:
            if self.conn:
                self.conn.close()
    
    def _create_tables(self):
        """ایجاد جداول اصلی"""
        tables = [
            # جدول کاربران
            """
            CREATE TABLE IF NOT EXISTS Users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username NVARCHAR(100) NOT NULL UNIQUE,
                Password NVARCHAR(255) NOT NULL,
                FullName NVARCHAR(200) NOT NULL,
                Role NVARCHAR(50) NOT NULL DEFAULT 'کاربر',
                IsActive BOOLEAN DEFAULT 1,
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # جدول مشتریان
            """
            CREATE TABLE IF NOT EXISTS Customers (
                CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
                CustomerCode NVARCHAR(50) UNIQUE,
                CustomerName NVARCHAR(200) NOT NULL,
                ContactPerson NVARCHAR(200),
                Phone NVARCHAR(20),
                Address TEXT,
                IsActive BOOLEAN DEFAULT 1,
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # جدول کالاها (محصولات)
            """
            CREATE TABLE IF NOT EXISTS Products (
                ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
                ProductCode NVARCHAR(50) UNIQUE,
                ProductName NVARCHAR(200) NOT NULL,
                ProductType NVARCHAR(100),  -- نوع جنس
                Unit NVARCHAR(20) DEFAULT 'متر',
                IsActive BOOLEAN DEFAULT 1,
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # جدول پارچه‌ها (اصلی)
            """
            CREATE TABLE IF NOT EXISTS Fabrics (
                FabricID INTEGER PRIMARY KEY AUTOINCREMENT,
                FabricCode NVARCHAR(50) UNIQUE NOT NULL,
                ProductID INTEGER,
                Meterage DECIMAL(10, 2) NOT NULL,  -- متراژ
                MachineNumber NVARCHAR(50),        -- شماره ماشین
                Weight DECIMAL(10, 2),            -- وزن
                WarpWeave NVARCHAR(100),          -- همبافت چله
                WeftWeave NVARCHAR(100),          -- همبافت پود
                WarpNumber NVARCHAR(100),         -- شماره چله
                WeaverName NVARCHAR(200),         -- نام بافنده
                DefectType NVARCHAR(200),         -- نوع خرابی
                ProductionDate DATE,              -- تاریخ تولید
                ProductionTime TIME,              -- زمان تولید
                CustomerID INTEGER,
                InvoiceNumber NVARCHAR(100),      -- شماره فاکتور
                InvoiceDate DATE,                 -- تاریخ فاکتور
                Status NVARCHAR(50) DEFAULT 'موجود',  -- وضعیت
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
                FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
            );
            """,
            
            # جدول ورود/خروج نخ
            """
            CREATE TABLE IF NOT EXISTS YarnTransactions (
                TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
                TransactionDate DATE NOT NULL,
                YarnType NVARCHAR(100) NOT NULL,      -- نوع نخ
                YarnWeave NVARCHAR(100),             -- همبافت نخ
                CustomerID INTEGER,
                InvoiceNumber NVARCHAR(100),         -- شماره فاکتور
                Weight DECIMAL(10, 2) NOT NULL,      -- وزن نخ
                MachineNumber NVARCHAR(50),          -- شماره ماشین
                WarpNumber NVARCHAR(100),            -- شماره چله
                TransactionType NVARCHAR(50) NOT NULL, -- 'ورودی' یا 'خروجی'
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
            );
            """,
            
            # جدول موجودی نخ
            """
            CREATE TABLE IF NOT EXISTS YarnInventory (
                InventoryID INTEGER PRIMARY KEY AUTOINCREMENT,
                YarnType NVARCHAR(100) NOT NULL,
                YarnWeave NVARCHAR(100) NOT NULL,
                CustomerID INTEGER,
                InitialStock DECIMAL(10, 2) DEFAULT 0,
                Incoming DECIMAL(10, 2) DEFAULT 0,
                Outgoing DECIMAL(10, 2) DEFAULT 0,
                CurrentStock DECIMAL(10, 2) GENERATED ALWAYS AS (InitialStock + Incoming - Outgoing),
                LastUpdated DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(YarnType, YarnWeave, CustomerID),
                FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
            );
            """,
            
            # جدول ماشین‌آلات
            """
            CREATE TABLE IF NOT EXISTS Machines (
                MachineID INTEGER PRIMARY KEY AUTOINCREMENT,
                MachineNumber NVARCHAR(50) UNIQUE NOT NULL,
                MachineName NVARCHAR(200),
                Status NVARCHAR(50) DEFAULT 'فعال',
                LastMaintenance DATE,
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # جدول گزارش‌ها
            """
            CREATE TABLE IF NOT EXISTS Reports (
                ReportID INTEGER PRIMARY KEY AUTOINCREMENT,
                ReportType NVARCHAR(100) NOT NULL,
                ReportDate DATE NOT NULL,
                Parameters TEXT,
                FilePath NVARCHAR(500),
                CreatedBy INTEGER,
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (CreatedBy) REFERENCES Users(UserID)
            );
            """
        ]
        
        cursor = self.conn.cursor()
        for table_sql in tables:
            cursor.execute(table_sql)
        
        self.conn.commit()
        print("📊 جداول ایجاد شدند")
    
    def _create_views(self):
        """ایجاد ویوهای گزارش‌گیری"""
        views = [
            # ویو گزارش پارچه‌های موجود
            """
            CREATE VIEW IF NOT EXISTS vw_AvailableFabrics AS
            SELECT 
                f.FabricCode,
                p.ProductName,
                f.Meterage,
                f.MachineNumber,
                f.Weight,
                f.WarpWeave,
                f.WeftWeave,
                f.WarpNumber,
                f.ProductionDate,
                c.CustomerName,
                f.Status
            FROM Fabrics f
            LEFT JOIN Products p ON f.ProductID = p.ProductID
            LEFT JOIN Customers c ON f.CustomerID = c.CustomerID
            WHERE f.Status = 'موجود'
            ORDER BY f.ProductionDate DESC;
            """,
            
            # ویو موجودی نخ
            """
            CREATE VIEW IF NOT EXISTS vw_YarnStock AS
            SELECT 
                yi.YarnType,
                yi.YarnWeave,
                c.CustomerName,
                yi.InitialStock,
                yi.Incoming,
                yi.Outgoing,
                yi.CurrentStock,
                CASE 
                    WHEN yi.CurrentStock < 0 THEN 'منفی'
                    WHEN yi.CurrentStock < yi.InitialStock * 0.2 THEN 'کمبود شدید'
                    WHEN yi.CurrentStock < yi.InitialStock * 0.5 THEN 'کمبود'
                    ELSE 'کافی'
                END AS StockStatus
            FROM YarnInventory yi
            LEFT JOIN Customers c ON yi.CustomerID = c.CustomerID
            ORDER BY yi.CurrentStock ASC;
            """
        ]
        
        cursor = self.conn.cursor()
        for view_sql in views:
            cursor.execute(view_sql)
        
        self.conn.commit()
        print("👁️ ویوهای گزارش‌گیری ایجاد شدند")
    
    def _insert_initial_data(self):
        """درج داده‌های اولیه"""
        cursor = self.conn.cursor()
        
        # کاربر پیش‌فرض
        cursor.execute("""
        INSERT OR IGNORE INTO Users (Username, Password, FullName, Role)
        VALUES ('admin', '123456', 'مدیر سیستم', 'مدیر')
        """)
        
        # مشتریان نمونه
        sample_customers = [
            ('C001', 'مشتری نمونه ۱', 'آقای احمدی', '021-12345678', 'تهران'),
            ('C002', 'مشتری نمونه ۲', 'آقای رضایی', '021-87654321', 'اصفهان'),
        ]
        
        for customer in sample_customers:
            cursor.execute("""
            INSERT OR IGNORE INTO Customers (CustomerCode, CustomerName, ContactPerson, Phone, Address)
            VALUES (?, ?, ?, ?, ?)
            """, customer)
        
        # محصولات نمونه
        sample_products = [
            ('P001', 'پارچه پنبه‌ای', 'پنبه'),
            ('P002', 'پارچه پلی‌استر', 'پلی‌استر'),
            ('P003', 'پارچه ویسکوز', 'ویسکوز'),
        ]
        
        for product in sample_products:
            cursor.execute("""
            INSERT OR IGNORE INTO Products (ProductCode, ProductName, ProductType)
            VALUES (?, ?, ?)
            """, product)
        
        # ماشین‌آلات نمونه
        for i in range(1, 16):
            cursor.execute("""
            INSERT OR IGNORE INTO Machines (MachineNumber, MachineName)
            VALUES (?, ?)
            """, (f'M{i}', f'ماشین شماره {i}'))
        
        self.conn.commit()
        print("📝 داده‌های اولیه درج شدند")

def migrate_excel_data(excel_path, db_path):
    """
    مهاجرت داده‌های اکسل به دیتابیس SQLite
    """
    print(f"🔄 در حال مهاجرت داده‌ها از {excel_path}...")
    
    try:
        conn = sqlite3.connect(db_path)
        
        # خواندن شیت‌های اکسل
        # (این بخش بستگی به ساختار فایل اکسل شما دارد)
        # مثال:
        # df_fabrics = pd.read_excel(excel_path, sheet_name='Sheet1')
        # df_fabrics.to_sql('Fabrics', conn, if_exists='append', index=False)
        
        print("✅ مهاجرت داده‌ها تکمیل شد")
        
    except Exception as e:
        print(f"❌ خطا در مهاجرت داده‌ها: {e}")

if __name__ == "__main__":
    # ایجاد پوشه‌ها
    os.makedirs('01_Database', exist_ok=True)
    os.makedirs('04_ExcelData/backup', exist_ok=True)
    os.makedirs('docs', exist_ok=True)
    
    # ایجاد دیتابیس
    creator = TextileDatabaseCreator('TextileDB.db')
    creator.create_database()
    
    print("\n🎉 دیتابیس آماده است!")
    print("📍 مسیر دیتابیس: TextileDB.db")
    print("📊 می‌توانید با ابزارهایی مانند DB Browser for SQLite آن را مشاهده کنید")