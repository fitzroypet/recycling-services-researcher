# Database Table Definitions

BUSINESS_TABLE = """
CREATE TABLE recycling.Businesses (
    BusinessID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(255) NOT NULL,
    FormattedAddress NVARCHAR(500) NOT NULL,
    Latitude DECIMAL(10, 8),
    Longitude DECIMAL(11, 8),
    PhoneNumber NVARCHAR(50),
    Website NVARCHAR(500),
    Rating DECIMAL(3, 2),
    PlaceID NVARCHAR(255),
    DateAdded DATETIME2 DEFAULT SYSUTCDATETIME(),
    LastUpdated DATETIME2 DEFAULT SYSUTCDATETIME(),
    IsActive BIT DEFAULT 1,
    DeletedAt DATETIME2 NULL,
    DeletedBy NVARCHAR(128) NULL,
    SearchVector NVARCHAR(MAX),
    ServiceKeywords NVARCHAR(MAX)
)
"""

ADDRESS_COMPONENT_TABLE = """
CREATE TABLE recycling.AddressComponents (
    AddressComponentID INT PRIMARY KEY IDENTITY(1,1),
    BusinessID INT,
    StreetAddress NVARCHAR(255),
    City NVARCHAR(100),
    State NVARCHAR(100),
    PostalCode NVARCHAR(20),
    Country NVARCHAR(100),
    FOREIGN KEY (BusinessID) REFERENCES recycling.Businesses(BusinessID)
)
"""

BUSINESS_HOURS_TABLE = """
CREATE TABLE recycling.BusinessHours (
    HoursID INT IDENTITY(1,1) PRIMARY KEY,
    BusinessID INT FOREIGN KEY REFERENCES recycling.Businesses(BusinessID),
    DayOfWeek TINYINT,  -- 0 = Sunday, 1 = Monday, etc.
    OpenTime TIME,
    CloseTime TIME,
    IsClosed BIT DEFAULT 0
)
"""

BUSINESS_MATERIALS_TABLE = """
CREATE TABLE recycling.BusinessMaterials (
    BusinessID INT,
    MaterialID INT,
    CategoryName NVARCHAR(50),
    Description NVARCHAR(500),
    IsVerified BIT DEFAULT 0,
    VerificationSource NVARCHAR(50),
    DateVerified DATETIME2,
    PRIMARY KEY (BusinessID, MaterialID),
    FOREIGN KEY (BusinessID) REFERENCES recycling.Businesses(BusinessID),
    FOREIGN KEY (MaterialID) REFERENCES recycling.Materials(MaterialID)
)
"""

BUSINESS_SERVICES_TABLE = """
CREATE TABLE recycling.BusinessServices (
    ServiceID INT IDENTITY(1,1) PRIMARY KEY,
    BusinessID INT FOREIGN KEY REFERENCES recycling.Businesses(BusinessID),
    ServiceName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500),
    IsBookingEnabled BIT DEFAULT 0,
    PriceInfo NVARCHAR(MAX), -- JSON field for flexible pricing structure
    CreatedDate DATETIME2 DEFAULT SYSUTCDATETIME(),
    ModifiedDate DATETIME2 DEFAULT SYSUTCDATETIME()
)
"""

MATERIALS_TABLE = """
CREATE TABLE recycling.Materials (
    MaterialID INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName NVARCHAR(50),
    Description NVARCHAR(500),
    CO2Savings DECIMAL(10, 2),
    CONSTRAINT UQ_Description UNIQUE (Description)
)
"""