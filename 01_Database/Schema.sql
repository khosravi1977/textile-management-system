-- طرح کامل دیتابیس به صورت جداگانه
-- فایل اصلی برای مستندات

-- :جدول کاربران
CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username NVARCHAR(100) NOT NULL UNIQUE,
    Password NVARCHAR(255) NOT NULL,
    FullName NVARCHAR(200) NOT NULL,
    Role NVARCHAR(50) NOT NULL DEFAULT 'کاربر',
    IsActive BOOLEAN DEFAULT 1,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- شاخص‌ها
CREATE INDEX idx_users_username ON Users(Username);
CREATE INDEX idx_users_role ON Users(Role);

-- :اطلاعات نمونه کاربران
INSERT INTO Users (Username, Password, FullName, Role) VALUES
('admin', '123456', 'مدیر سیستم', 'مدیر'),
('operator', '123456', 'اپراتور تولید', 'اپراتور'),
('accountant', '123456', 'حسابدار', 'حسابدار');

-- ادامه جداول مشابه بالا...